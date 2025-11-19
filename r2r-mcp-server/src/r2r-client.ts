/**
 * R2R API Client for MCP Server
 */

import fetch from 'node-fetch';
import FormData from 'form-data';
import * as fs from 'fs';
import type {
  IngestArgs,
  SearchArgs,
  RAGArgs,
  KGSearchArgs,
  ListDocumentsArgs,
} from './types/r2r-types.js';

export class R2RClient {
  private baseUrl: string;
  private authToken: string | null;

  constructor(baseUrl?: string, authToken?: string) {
    this.baseUrl = baseUrl || process.env.R2R_BASE_URL || 'http://136.119.36.216:7272';
    this.authToken = authToken || process.env.R2R_AUTH_TOKEN || null;
  }

  /**
   * Get authorization headers
   */
  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.authToken) {
      headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    return headers;
  }

  /**
   * Login to R2R and get access token
   */
  async login(email: string, password: string): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/v2/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Login failed: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      // Store the access token
      if (data.results?.access_token?.token) {
        this.authToken = data.results.access_token.token;
      }

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                status: 'success',
                message: 'Logged in successfully',
                token: this.authToken,
                expires_at: data.results?.access_token?.expires_at,
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error logging in: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * Ingest a document into R2R (async operation)
   */
  async ingestDocument(args: IngestArgs) {
    try {
      const formData = new FormData();

      if (args.file_path) {
        // Check if file exists
        if (!fs.existsSync(args.file_path)) {
          throw new Error(`File not found: ${args.file_path}`);
        }
        formData.append('file', fs.createReadStream(args.file_path));
      } else if (args.chunks) {
        // Ingest pre-processed chunks
        formData.append('chunks', JSON.stringify(args.chunks));
      } else {
        throw new Error('Either file_path or chunks must be provided');
      }

      formData.append('ingestion_mode', args.mode || 'fast');

      if (args.metadata) {
        formData.append('metadata', JSON.stringify(args.metadata));
      }

      const headers: Record<string, string> = {};
      if (this.authToken) {
        headers['Authorization'] = `Bearer ${this.authToken}`;
      }

      const response = await fetch(`${this.baseUrl}/v3/documents`, {
        method: 'POST',
        headers,
        body: formData as any,
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                status: 'success',
                message: 'Document ingestion started (async operation)',
                document_id: data.results?.[0]?.document_id || 'unknown',
                ingestion_mode: args.mode || 'fast',
                note: 'Ingestion is processing in background. Use r2r_list_documents to check status.',
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error ingesting document: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * Search documents using vector/hybrid search
   */
  async search(args: SearchArgs) {
    try {
      const searchSettings: any = {
        search_mode: args.mode || 'advanced',
        limit: args.limit || 10,
      };

      if (args.use_hybrid_search !== undefined) {
        searchSettings.use_hybrid_search = args.use_hybrid_search;
      }

      if (args.filters) {
        searchSettings.filters = args.filters;
      }

      const response = await fetch(`${this.baseUrl}/v3/retrieval/search`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          query: args.query,
          search_settings: searchSettings,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      // Format results for better readability
      const results = data.results?.chunk_search_results || [];
      const formattedResults = results.map((chunk: any, index: number) => ({
        rank: index + 1,
        score: chunk.score,
        text: chunk.text?.substring(0, 300) + (chunk.text?.length > 300 ? '...' : ''),
        document: chunk.metadata?.title || chunk.metadata?.document_id || 'Unknown',
        metadata: chunk.metadata,
      }));

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                query: args.query,
                total_results: formattedResults.length,
                results: formattedResults,
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error searching documents: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * RAG query with optional streaming
   */
  async rag(args: RAGArgs) {
    try {
      const requestBody: any = {
        query: args.query,
      };

      if (args.search_settings) {
        requestBody.search_settings = args.search_settings;
      }

      if (args.rag_generation_config) {
        requestBody.rag_generation_config = args.rag_generation_config;
      }

      const endpoint = args.stream
        ? `${this.baseUrl}/v3/retrieval/rag?stream=true`
        : `${this.baseUrl}/v3/retrieval/rag`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      if (args.stream) {
        // Handle streaming response
        let fullText = '';
        const decoder = new TextDecoder();

        if (!response.body) {
          throw new Error('Response body is null');
        }

        // Node.js ReadableStream handling
        for await (const chunk of response.body as any) {
          fullText += decoder.decode(chunk, { stream: true });
        }

        return {
          content: [
            {
              type: 'text',
              text: fullText,
            },
          ],
        };
      } else {
        const data = await response.json() as any;

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                {
                  query: args.query,
                  answer: data.results?.completion || data.results,
                  sources: data.results?.search_results?.chunk_search_results?.length || 0,
                },
                null,
                2
              ),
            },
          ],
        };
      }
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error performing RAG query: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * Knowledge graph search
   */
  async kgSearch(args: KGSearchArgs) {
    try {
      const response = await fetch(`${this.baseUrl}/v3/retrieval/search`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          query: args.query,
          graph_search_settings: {
            use_graph_search: true,
            kg_search_type: args.kg_search_type || 'local',
          },
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(data.results, null, 2),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error performing knowledge graph search: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * List all documents
   */
  async listDocuments(args: ListDocumentsArgs = {}) {
    try {
      const limit = args.limit || 100;
      const offset = args.offset || 0;

      const response = await fetch(`${this.baseUrl}/v3/documents?limit=${limit}&offset=${offset}`, {
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      // Format for better readability
      const documents = data.results || [];
      const formattedDocs = documents.map((doc: any) => ({
        id: doc.id,
        title: doc.title,
        type: doc.type,
        status: doc.ingestion_status,
        created: doc.created_at,
        metadata: doc.metadata,
      }));

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                total: formattedDocs.length,
                limit,
                offset,
                documents: formattedDocs,
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error listing documents: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  /**
   * Delete a document
   */
  async deleteDocument(documentId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/v3/documents/${documentId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`R2R API error: ${response.status} - ${error}`);
      }

      const data = await response.json() as any;

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                status: 'success',
                message: 'Document deleted successfully',
                document_id: documentId,
              },
              null,
              2
            ),
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: 'text',
            text: `Error deleting document: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }
}
