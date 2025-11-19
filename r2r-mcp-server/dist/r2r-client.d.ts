/**
 * R2R API Client for MCP Server
 */
import type { IngestArgs, SearchArgs, RAGArgs, KGSearchArgs, ListDocumentsArgs } from './types/r2r-types.js';
export declare class R2RClient {
    private baseUrl;
    private authToken;
    constructor(baseUrl?: string, authToken?: string);
    /**
     * Get authorization headers
     */
    private getAuthHeaders;
    /**
     * Login to R2R and get access token
     */
    login(email: string, password: string): Promise<any>;
    /**
     * Ingest a document into R2R (async operation)
     */
    ingestDocument(args: IngestArgs): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
    /**
     * Search documents using vector/hybrid search
     */
    search(args: SearchArgs): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
    /**
     * RAG query with optional streaming
     */
    rag(args: RAGArgs): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
    /**
     * Knowledge graph search
     */
    kgSearch(args: KGSearchArgs): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
    /**
     * List all documents
     */
    listDocuments(args?: ListDocumentsArgs): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
    /**
     * Delete a document
     */
    deleteDocument(documentId: string): Promise<{
        content: {
            type: string;
            text: string;
        }[];
        isError?: undefined;
    } | {
        content: {
            type: string;
            text: string;
        }[];
        isError: boolean;
    }>;
}
