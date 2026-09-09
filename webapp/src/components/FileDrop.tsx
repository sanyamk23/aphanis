import { useRef, useState } from "react";
import { api } from "../api";
import type { Mode } from "../types";

const ACCEPT = ".txt,.md,.py,.js,.ts,.json,.html,.svg,.docx,.pptx,.xlsx,.ipynb,.pdf,.png,.jpg,.jpeg";

export default function FileDrop({ onTextLoaded }: { onTextLoaded: (t: string) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(f: File) {
    setFile(f);
    setStatus(null);
    const ext = f.name.split(".").pop()?.toLowerCase() ?? "";
    const isText = ["txt", "md", "py", "js", "ts", "json", "html", "svg", "csv"].includes(ext);

    if (isText) {
      const text = await f.text();
      onTextLoaded(text);
      setStatus(`Loaded ${f.name}`);
    } else {
      // Binary: upload to engine for cleaning
      setBusy(true);
      try {
        const res = await api.cleanFile(f, "paranoid" as Mode, false, false);
        setStatus(res.message);
        if (res.success && res.data_base64) {
          const blob = new Blob(
            [Uint8Array.from(atob(res.data_base64), (c) => c.charCodeAt(0))],
            { type: "application/octet-stream" },
          );
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `aphanis_${res.filename}`;
          a.click();
          URL.revokeObjectURL(url);
        }
      } catch (e) {
        setStatus((e as Error).message);
      } finally {
        setBusy(false);
      }
    }
  }

  return (
    <div
      className="card file-drop"
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        const f = e.dataTransfer.files?.[0];
        if (f) handleFile(f);
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        style={{ display: "none" }}
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) handleFile(f);
        }}
      />
      <div className="drop-zone">
        <div className="drop-icon">📂</div>
        <p>
          <strong>Drop a file</strong> or click to upload
        </p>
        <small>Text files are scanned in-browser. Images, DOCX, PDF, IPYNB are cleaned server-side.</small>
        {file && <div className="file-name">{file.name}</div>}
        {busy && <div className="file-status">Cleaning…</div>}
        {status && !busy && <div className="file-status">{status}</div>}
      </div>
    </div>
  );
}
