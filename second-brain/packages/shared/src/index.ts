export const API_VERSION = "v1" as const;

export type ErrorCode = string;

export interface FieldError {
  field: string;
  code: string;
  message?: string;
}

export interface ErrorEnvelope {
  code: ErrorCode;
  message: string;
  trace_id: string;
  field_errors?: FieldError[];
}

export type DocumentStatus =
  | "QUEUED"
  | "PROCESSING"
  | "READY"
  | "ERROR"
  | "DEAD_LETTER"
  | "DELETED";

export interface DocumentRecord {
  id: string;
  owner_id: string;
  name: string;
  status: DocumentStatus;
  created_at: string;
  ingestion_version?: string;
}

export type ChatEventType =
  | "token"
  | "citation"
  | "tool_status"
  | "confirmation_required"
  | "final"
  | "error";

export interface ChatEvent {
  type: ChatEventType;
  conversation_id: string;
  trace_id: string;
  data?: Record<string, unknown>;
}
