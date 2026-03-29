# Learn Challenge And Grow

## Native Tool Requirement (Poppler & Tesseract)

This project performs advanced PDF processing, including text‑based PDFs, scanned PDFs (OCR), and future vision / multimodal document understanding use cases. To ensure the solution works reliably in **restricted or enterprise environments** (where admin rights are unavailable), the project intentionally avoids system‑level installations and instead relies on **portable native binaries** bundled directly with the codebase.

Python libraries such as `pdf2image` and `pytesseract` are **only wrappers**. They do not implement PDF rendering or OCR logic themselves and require external native tools to function correctly.

The following native tools are mandatory:


| Tool              | Used By       | Purpose                                                                                          | Download Location                                          |
| ----------------- | ------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| **Poppler**       | `pdf2image`   | Converts PDF pages into images. Required for scanned PDFs and image‑based processing pipelines. | https://github.com/oschwartz10612/poppler-windows/releases |
| **Tesseract OCR** | `pytesseract` | Performs Optical Character Recognition to extract text from PDF images.                          | https://github.com/UB-Mannheim/tesseract/wiki              |

These tools must be downloaded as **portable / ZIP builds only**. Do **not** use installers if admin rights are unavailable.

Once downloaded, extract the required binaries and place them under a `tools/` directory at the project root, following the structure below:

project-root/
├─ tools/
│  ├─ poppler/
│  │   └─ bin/
│  │       ├─ pdfinfo.exe
│  │       └─ pdftoppm.exe
│  │
│  └─ tesseract/
│      ├─ tesseract.exe
│      ├─ *.dll
│      └─ tessdata/
│          └─ eng.traineddata

The application dynamically resolves these paths at runtime and explicitly binds Python wrappers to the local binaries. `pdf2image` is configured with the Poppler `bin` directory, and `pytesseract` is configured with the local `tesseract.exe`. No environment variables, registry changes, or system PATH updates are required.

Before running OCR or scanned‑PDF workflows, ensure the following files exist:

- `tools/poppler/bin/pdfinfo.exe`
- `tools/poppler/bin/pdftoppm.exe`
- `tools/tesseract/tesseract.exe`
- `tools/tesseract/tessdata/eng.traineddata`

If the above files are present, no further setup is needed. This approach mirrors **production‑grade document AI systems**, ensuring deterministic execution across developer machines, CI/CD pipelines, and locked‑down corporate environments while enabling OCR, vision‑based processing, and future RAG workflows.

The application dynamically resolves these paths at runtime and explicitly binds Python wrappers to the local binaries. `pdf2image` is configured with the Poppler `bin` directory, and `pytesseract` is configured with the local `tesseract.exe`. No environment variables, registry changes, or system PATH updates are required.

Before running OCR or scanned‑PDF workflows, ensure the following files exist:

- `tools/poppler/bin/pdfinfo.exe`
- `tools/poppler/bin/pdftoppm.exe`
- `tools/tesseract/tesseract.exe`
- `tools/tesseract/tessdata/eng.traineddata`

If the above files are present, no further setup is needed. This approach mirrors **production‑grade document AI systems**, ensuring deterministic execution across developer machines, CI/CD pipelines, and locked‑down corporate environments while enabling OCR, vision‑based processing, and future RAG workflows.

PDF Pipeline
├─ pypdf / pdfplumber
├─ pdf2image + pytesseract
├─ (later) vision models
└─ → produces PageDocuments (text + metadata)
↓
LangChain
├─ Text splitter
├─ Vector store
├─ Retriever
└─ LLM chains / agents
