/**
 * R2R API Type Definitions
 */

export interface R2RDocument {
  id: string;
  title: string;
  user_id: string;
  type: string;
  created_at: string;
  updated_at: string;
  ingestion_status: 'pending' | 'processing' | 'success' | 'failed';
  restructuring_status: string;
  version: string;
  metadata: Record<string, any>;
  collection_ids?: string[];
}

export interface SearchChunk {
  text: string;
  score: number;
  metadata: {
    document_id?: string;
    title?: string;
    [key: string]: any;
  };
}

export interface SearchResult {
  chunk_search_results: SearchChunk[];
}

export interface RAGResult {
  completion: string;
  search_results?: SearchResult;
}

export interface IngestArgs {
  file_path: string;
  mode?: 'fast' | 'hi-res' | 'custom';
  metadata?: Record<string, any>;
  chunks?: string[];
}

export interface SearchArgs {
  query: string;
  mode?: 'basic' | 'advanced' | 'custom';
  limit?: number;
  filters?: Record<string, any>;
  use_hybrid_search?: boolean;
}

export interface RAGArgs {
  query: string;
  stream?: boolean;
  search_settings?: {
    search_mode?: string;
    limit?: number;
    use_hybrid_search?: boolean;
    filters?: Record<string, any>;
  };
  rag_generation_config?: {
    model?: string;
    temperature?: number;
    max_tokens?: number;
  };
}

export interface KGSearchArgs {
  query: string;
  kg_search_type?: 'local' | 'global';
}

export interface ListDocumentsArgs {
  limit?: number;
  offset?: number;
}
