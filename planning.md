# planning.md

## Domain
Unofficial student reviews of Computer Systems Technology (CST) professors at 
New York City College of Technology (City Tech), sourced from Rate My Professors. 

This knowledge is valuable because official channels — course catalogs, faculty 
pages, and advisors — describe what a course covers but not what it's actually 
like to take it. Students need to know whether a professor's exams are fair, 
whether attendance is enforced, and whether they explain concepts clearly. That 
knowledge lives exclusively in peer reviews and is impossible to search by 
specific question.

## Documents
| File | Professor | Source |
|------|-----------|--------|
| prof_franklin_cst.txt | Warren Franklin | Rate My Professors |
| prof_sharma_cst.txt | Deodat Sharma | Rate My Professors |
| prof_belich_cst.txt | Sergio Belich | Rate My Professors |
| prof_natarajan_cst.txt | Nithya Natarajan | Rate My Professors |
| prof_kalia_cst.txt | Suman Kalia | Rate My Professors |

## Chunking Strategy
- **Chunk size:** 600 characters
- **Overlap:** 100 characters
- **Rationale:** RMP reviews are short and self-contained (2–5 sentences). 
  At 600 characters, most individual reviews fit within a single chunk. 
  Overlap is minimal because reviews don't flow into each other.

## Retrieval Approach
- **Embedding model:** all-MiniLM-L6-v2 via sentence-transformers
- **Vector store:** ChromaDB (local)
- **Top-k:** 5 chunks per query
- **Production tradeoffs:** text-embedding-3-large for longer context; 
  domain-specific fine-tuning for better accuracy on academic review text.

## Evaluation Plan
| # | Question | Expected Answer |
|---|----------|-----------------|
| 1 | What do students say about Warren Franklin's exams? | Exam format, difficulty, hints given in class |
| 2 | Is Deodat Sharma recommended for CST students? | Positive recommendation, must work hard |
| 3 | What is Sergio Belich's teaching style like? | Textbook-based lectures, mixed reviews |
| 4 | How does Nithya Natarajan grade assignments? | Tough grader, exam-focused |
| 5 | What do students say about Suman Kalia's workload? | Workload details from Kalia reviews |

## Anticipated Challenges
1. Short chunks with low semantic signal — brief reviews may not carry enough 
   meaning for precise embedding matching.
2. Professor name ambiguity — queries about one professor may surface chunks 
   from other documents if reviews mention similar names or topics.

## Architecture

Raw .txt files (5 professor review files)
│
▼
[ Document Ingestion ]
Load files from disk — Python (open/read)
│
▼
[ Cleaning ]
Remove blank lines, extra whitespace — Python regex
│
▼
[ Chunking ]
600 chars, 100 overlap — LangChain RecursiveCharacterTextSplitter
│
▼
[ Embedding + Vector Store ]
all-MiniLM-L6-v2 + ChromaDB
│
▼
[ Retrieval ]
Top-5 semantic similarity — ChromaDB query()
│
▼
[ Generation ]
Grounded response — Groq llama-3.3-70b-versatile
│
▼
[ Query Interface ]
Gradio web UI

## AI Tool Plan
| Stage | Input to AI | Expected Output |
|-------|-------------|-----------------|
| Ingestion + Cleaning | Documents section + chunking strategy | ingest.py that loads and cleans all 5 .txt files |
| Chunking | Chunking strategy + sample text | chunk_text() using RecursiveCharacterTextSplitter |
| Embedding + Vector Store | Architecture diagram + retrieval section | embed.py with ChromaDB storage and source metadata |
| Retrieval | ChromaDB setup + top-k spec | retrieve() function returning top-5 chunks with sources |
| Generation | Retrieval function + grounding requirement | Prompt template and ask() function |
| Interface | ask() function + output format | Gradio app with question input, answer and sources output |