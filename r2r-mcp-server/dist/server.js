#!/usr/bin/env node
/**
 * R2R MCP Server
 *
 * Provides Claude Code integration with R2R RAG system via Model Context Protocol
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema, } from '@modelcontextprotocol/sdk/types.js';
import { R2RClient } from './r2r-client.js';
const R2R_BASE_URL = process.env.R2R_BASE_URL || 'http://136.119.36.216:7272';
const R2R_AUTH_TOKEN = process.env.R2R_AUTH_TOKEN;
const r2rClient = new R2RClient(R2R_BASE_URL, R2R_AUTH_TOKEN);
const server = new Server({
    name: 'r2r-mcp-server',
    version: '1.0.0',
}, {
    capabilities: {
        tools: {},
    },
});
// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: 'r2r_login',
                description: 'Login to R2R API and obtain access token. Required for authenticated operations. Returns access token that is automatically used for subsequent requests.',
                inputSchema: {
                    type: 'object',
                    properties: {
                        email: {
                            type: 'string',
                            description: 'User email address',
                        },
                        password: {
                            type: 'string',
                            description: 'User password',
                        },
                    },
                    required: ['email', 'password'],
                },
            },
            {
                name: 'r2r_ingest',
                description: 'Ingest documents into R2R for indexing and RAG. This is an ASYNC operation - returns immediately with document_id. Use r2r_list_documents to check ingestion status. Supports modes: fast (quick), hi-res (detailed), custom (full control).',
                inputSchema: {
                    type: 'object',
                    properties: {
                        file_path: {
                            type: 'string',
                            description: 'Absolute path to file to ingest',
                        },
                        mode: {
                            type: 'string',
                            enum: ['fast', 'hi-res', 'custom'],
                            default: 'fast',
                            description: 'Ingestion mode: fast (speed), hi-res (quality), custom (full control)',
                        },
                        metadata: {
                            type: 'object',
                            description: 'Optional metadata to attach to document (e.g., tags, source, author)',
                        },
                        chunks: {
                            type: 'array',
                            items: { type: 'string' },
                            description: 'Pre-processed text chunks (alternative to file_path)',
                        },
                    },
                },
            },
            {
                name: 'r2r_search',
                description: 'Search indexed documents using vector/hybrid search. Fast synchronous operation. Returns ranked results with scores and metadata. Modes: basic (semantic only), advanced (hybrid), custom (full control).',
                inputSchema: {
                    type: 'object',
                    properties: {
                        query: {
                            type: 'string',
                            description: 'Search query or question',
                        },
                        mode: {
                            type: 'string',
                            enum: ['basic', 'advanced', 'custom'],
                            default: 'advanced',
                            description: 'Search mode: basic (semantic), advanced (hybrid), custom (manual)',
                        },
                        limit: {
                            type: 'number',
                            default: 10,
                            description: 'Maximum number of results to return',
                        },
                        use_hybrid_search: {
                            type: 'boolean',
                            description: 'Enable hybrid search (semantic + keyword)',
                        },
                        filters: {
                            type: 'object',
                            description: 'Optional filters (e.g., {"title": {"$in": ["doc1.pdf"]}})',
                        },
                    },
                    required: ['query'],
                },
            },
            {
                name: 'r2r_rag',
                description: 'Retrieval-Augmented Generation query. Searches indexed documents and generates AI answer using LLM. Supports streaming for real-time responses. Returns answer with source citations.',
                inputSchema: {
                    type: 'object',
                    properties: {
                        query: {
                            type: 'string',
                            description: 'Question to answer using RAG',
                        },
                        stream: {
                            type: 'boolean',
                            default: false,
                            description: 'Enable streaming for real-time token delivery',
                        },
                        search_settings: {
                            type: 'object',
                            description: 'Search configuration (mode, limit, filters)',
                            properties: {
                                search_mode: { type: 'string' },
                                limit: { type: 'number' },
                                use_hybrid_search: { type: 'boolean' },
                                filters: { type: 'object' },
                            },
                        },
                        rag_generation_config: {
                            type: 'object',
                            description: 'LLM generation settings (model, temperature, max_tokens)',
                            properties: {
                                model: { type: 'string' },
                                temperature: { type: 'number' },
                                max_tokens: { type: 'number' },
                            },
                        },
                    },
                    required: ['query'],
                },
            },
            {
                name: 'r2r_kg_search',
                description: 'Knowledge graph search for entity relationships and graph-based queries. Explores connections between entities extracted from documents. Types: local (entity-centric), global (graph-wide).',
                inputSchema: {
                    type: 'object',
                    properties: {
                        query: {
                            type: 'string',
                            description: 'Entity or relationship query',
                        },
                        kg_search_type: {
                            type: 'string',
                            enum: ['local', 'global'],
                            default: 'local',
                            description: 'KG search type: local (entity-focused), global (graph-wide)',
                        },
                    },
                    required: ['query'],
                },
            },
            {
                name: 'r2r_list_documents',
                description: 'List all indexed documents with their ingestion status. Use this to check if async ingestion completed. Returns document metadata, status (pending/processing/success/failed), and timestamps.',
                inputSchema: {
                    type: 'object',
                    properties: {
                        limit: {
                            type: 'number',
                            default: 100,
                            description: 'Maximum documents to return',
                        },
                        offset: {
                            type: 'number',
                            default: 0,
                            description: 'Pagination offset',
                        },
                    },
                },
            },
            {
                name: 'r2r_delete_document',
                description: 'Delete a document from R2R. Cascading deletion: removes document, chunks, embeddings, and KG entries. Use document_id from r2r_list_documents.',
                inputSchema: {
                    type: 'object',
                    properties: {
                        document_id: {
                            type: 'string',
                            description: 'UUID of document to delete',
                        },
                    },
                    required: ['document_id'],
                },
            },
        ],
    };
});
// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        switch (name) {
            case 'r2r_login':
                return await r2rClient.login(args.email, args.password);
            case 'r2r_ingest':
                return await r2rClient.ingestDocument(args);
            case 'r2r_search':
                return await r2rClient.search(args);
            case 'r2r_rag':
                return await r2rClient.rag(args);
            case 'r2r_kg_search':
                return await r2rClient.kgSearch(args);
            case 'r2r_list_documents':
                return await r2rClient.listDocuments(args);
            case 'r2r_delete_document':
                return await r2rClient.deleteDocument(args.document_id);
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    }
    catch (error) {
        return {
            content: [
                {
                    type: 'text',
                    text: `Error: ${error.message}`,
                },
            ],
            isError: true,
        };
    }
});
// Start server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('R2R MCP Server running on stdio');
    console.error(`Connected to R2R at: ${R2R_BASE_URL}`);
}
main().catch((error) => {
    console.error('Fatal server error:', error);
    process.exit(1);
});
