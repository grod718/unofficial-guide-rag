\# planning.md



\## Domain

Unofficial student reviews of Computer Systems Technology (CST) professors at 

New York City College of Technology (City Tech), sourced from Rate My Professors. 



This knowledge is valuable because official channels — course catalogs, faculty 

pages, and advisors — describe what a course covers but not what it's actually 

like to take it. Students need to know whether a professor's exams are fair, 

whether attendance is enforced, and whether they explain concepts clearly. That 

knowledge lives exclusively in peer reviews and is impossible to search by 

specific question.



\## Documents

Five professor review pages collected manually from Rate My Professors. Each 

document contains all available written reviews for one CST professor at City Tech.



| File | Professor | Source URL |

|------|-----------|------------|

| `prof\_franklin\_cst.txt` | Warren Franklin | https://www.ratemyprofessors.com/https://www.ratemyprofessors.com/professor/262472| `prof\_sharma\_cst.txt` | Deodat Sharma | https://www.ratemyprofessors.com/https://www.ratemyprofessors.com/professor/2327943 |

| `prof\_belich\_cst.txt` | Sergio Belich | https://www.ratemyprofessors.com/https://www.ratemyprofessors.com/professor/2309194 |

| `prof\_natarajan\_cst.txt` | Nithya Natarajan | https://www.ratemyprofessors.com/https://www.ratemyprofessors.com/professor/1866564 |

| `prof\_kalia\_cst.txt` | Suman Kalia | https://www.ratemyprofessors.com/https://www.ratemyprofessors.com/professor/1383683 |



Each file contains: written review text, course tags where visible, and any 

student-flagged attributes (e.g., "tough grader," "attendance mandatory").



\## Chunking Strategy

RMP reviews are short and self-contained — typically 2–5 sentences per review. 

Each review represents a complete, standalone opinion and should not be merged 

with adjacent reviews or split mid-sentence.



\- \*\*Chunk size:\*\* 400 characters

\- \*\*Overlap:\*\* 50 characters

\- \*\*Rationale:\*\* At 400 characters, most individual reviews fit within a single 

&#x20; chunk, preserving the complete thought. Overlap is kept minimal (50 characters) 

&#x20; because reviews don't flow into each other — there is no narrative continuity 

&#x20; across review boundaries. Chunks that are too large (e.g., 1000+ characters) 

&#x20; would merge multiple reviews about different topics (exams, attendance, grading) 

&#x20; into one embedding, making it impossible to match a specific query precisely. 

&#x20; Chunks that are too small (under 150 characters) would produce fragments without 

&#x20; enough semantic signal for the embedding model to differentiate.



\## Retrieval Approach

\- \*\*Embedding model:\*\* `all-MiniLM-L6-v2` via `sentence-transformers` (runs 

&#x20; locally, no API key required)

\- \*\*Vector store:\*\* ChromaDB (local, no account needed)

\- \*\*Top-k:\*\* 5 chunks per query



\*\*Why k=5:\*\* Five chunks gives the LLM enough context to synthesize an answer 

across multiple reviews without overwhelming it with loosely related content. 

Too few (k=2) risks missing the most relevant review if it wasn't the closest 

match. Too many (k=10+) dilutes the context with tangentially related chunks.



\*\*Production tradeoffs (if cost weren't a constraint):\*\*

\- \*Context length:\* `all-MiniLM-L6-v2` handles up to 256 tokens — fine for 

&#x20; short reviews, but a model like `text-embedding-3-large` (OpenAI) supports 

&#x20; longer context for multi-paragraph documents.

\- \*Accuracy:\* Domain-specific embeddings (e.g., fine-tuned on academic text) 

&#x20; would likely outperform a general-purpose model on educational review language.

\- \*Latency:\* Local models add no API latency but are slower on CPU than 

&#x20; cloud-based embeddings at scale.

\- \*Multilingual:\* Not a concern for this corpus — all reviews are in English.



\## Evaluation Plan



| # | Test Question | Expected Answer |

|---|---------------|-----------------|

| 1 | What do students say about Warren Franklin's exams? | Reviews should describe exam format, difficulty, and whether material is curved or fair |

| 2 | Is Deodat Sharma recommended for CST students? | Aggregate sentiment from reviews — positive, mixed, or negative recommendation |

| 3 | What is Sergio Belich's teaching style like? | Reviews should describe clarity of explanation, lecture style, and student engagement |

| 4 | How does Nithya Natarajan grade assignments? | Reviews should describe grading strictness, rubric clarity, and feedback quality |

| 5 | What do students say about Suman Kalia's workload? | Reviews should describe homework volume, project expectations, and time commitment |



\## Anticipated Challenges



1\. \*\*Short chunks with low semantic signal:\*\* RMP reviews are often very brief 

&#x20;  ("Great professor, highly recommend"). At 400 characters, some chunks may not 

&#x20;  carry enough meaning for the embedding model to distinguish between professors 

&#x20;  on specific topics like grading vs. teaching style.



2\. \*\*Professor name ambiguity in retrieval:\*\* A query about "Franklin" could 

&#x20;  theoretically surface chunks from another document if a review mentions a 

&#x20;  different person by that name. Source metadata filtering will be essential to 

&#x20;  ensure attribution is accurate.



\## Architecture

