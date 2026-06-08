# \# City Tech CST Unofficial Professor Guide

# 

# A RAG (Retrieval-Augmented Generation) system that makes student reviews of 

# Computer Systems Technology professors at New York City College of Technology 

# searchable and answerable using plain-language questions.

# 

# \## Domain

# 

# Unofficial student reviews of CST professors at City Tech, sourced from Rate 

# My Professors. This knowledge is valuable because official channels describe 

# credentials and course content — not whether a professor's exams are fair, 

# whether attendance is enforced, or whether they respond to emails. That 

# knowledge lives exclusively in peer reviews and is impossible to search by 

# specific question.

# 

# Professors covered:

# \- Warren Franklin

# \- Deodat Sharma

# \- Sergio Belich

# \- Nithya Natarajan

# \- Suman Kalia

# 

# \## Document Sources

# 

# | File | Professor | Source |

# |------|-----------|--------|

# | prof\_franklin\_cst.txt | Warren Franklin | Rate My Professors |

# | prof\_sharma\_cst.txt | Deodat Sharma | Rate My Professors |

# | prof\_belich\_cst.txt | Sergio Belich | Rate My Professors |

# | prof\_natarajan\_cst.txt | Nithya Natarajan | Rate My Professors |

# | prof\_kalia\_cst.txt | Suman Kalia | Rate My Professors |

# 

# \## Chunking Strategy

# 

# \- \*\*Chunk size:\*\* 600 characters

# \- \*\*Overlap:\*\* 100 characters

# \- \*\*Splitter:\*\* RecursiveCharacterTextSplitter (LangChain)

# \- \*\*Filter:\*\* Chunks under 100 characters or with fewer than 3 words longer 

# &#x20; than 5 characters are discarded as metadata-only fragments

# \- \*\*Total chunks:\*\* 55

# 

# \*\*Reasoning:\*\* RMP reviews are short and self-contained (2–5 sentences each). 

# At 600 characters, most individual reviews fit within a single chunk, preserving 

# the complete opinion. Overlap is kept at 100 characters because reviews don't 

# flow into each other — there is no narrative continuity across review boundaries.

# 

# \## Sample Chunks

# 

\*\*Chunk 1 — prof\_belich\_cst.txt\*\*

CST3519 Dec 29th, 2021 For Credit: Yes Attendance: Not Mandatory Would Take
===

# Again: No Grade: A Professor Belich is a nice, well meaning guy but his teaching

# style isnt that great. He teaches straight from the textbook during lectures

# which makes it tough to actually learn anything or stay focused \& engaged in

# class. His exams are basically HW questions, so DO YOUR HW!

# 

# \*\*Chunk 2 — prof\_franklin\_cst.txt\*\*

# CST2206 Jun 9th, 2025 For Credit: Yes Attendance: Mandatory Would Take Again:

# Yes Grade: A Reviews on this Site = On Target, One of the Best Professors,

# Great Discussions of Current Tech Topics.

# 

# \*\*Chunk 3 — prof\_kalia\_cst.txt\*\*

# CST2410 Mar 3rd, 2023 For Credit: Yes Attendance: Mandatory Would Take Again:

# Yes Grade: Not sure yet excellent professor. very easy going and funny.

# Amazing lectures Clear grading criteria

# 

# \*\*Chunk 4 — prof\_natarajan\_cst.txt\*\*

# CST2406 May 24th, 2024 For Credit: Yes Attendance: Mandatory Would Take Again:

# Yes Grade: A- I would take the class if you are willing to go through her

# lectures and study. Her exams are easy as long as you pay attention to what

# she did in class or go over the recording.

# 

# \*\*Chunk 5 — prof\_sharma\_cst.txt\*\*

# For Credit: Yes Attendance: Mandatory Grade: Not sure yet He holds time for

# questions but doesn't answer them directly. Will not take time for individuals

# during the class. BEWARE, he will express in person things are OK to be done

# one way and will grade you as if the conversation never happened.

# 

# \## Embedding Model

# 

# \- \*\*Model:\*\* `all-MiniLM-L6-v2` via `sentence-transformers`

# \- \*\*Vector store:\*\* ChromaDB (local, persistent)

# \- \*\*Top-k:\*\* 5 chunks per query

# 

# \*\*Production tradeoffs:\*\*

# \- \*Context length:\* all-MiniLM-L6-v2 handles up to 256 tokens — fine for short 

# &#x20; reviews, but a model like text-embedding-3-large (OpenAI) supports longer context.

# \- \*Accuracy:\* A model fine-tuned on academic or review text would likely 

# &#x20; outperform a general-purpose model on this domain.

# \- \*Cost:\* all-MiniLM-L6-v2 runs locally with no API cost or rate limits — 

# &#x20; ideal for a project of this scale.

# \- \*Latency:\* Local inference adds no API latency but is slower on CPU at scale.

# 

# \## Retrieval Test Results

# 

# \*\*Query 1: "What do students say about exams?"\*\*

# \- Result 1: prof\_belich\_cst.txt — "The midterm and finals are 80% of the grade" ✅ Relevant

# \- Result 2: prof\_franklin\_cst.txt — "the two exams were online and also easy" ✅ Relevant

# \- Result 3: prof\_sharma\_cst.txt — general teaching style review ⚠️ Loosely relevant

# 

# \*\*Query 2: "What is Belich's teaching style?"\*\*

# \- Result 1: prof\_belich\_cst.txt — "teaches straight from the textbook" ✅ Relevant

# \- Result 2: prof\_belich\_cst.txt — "explains everything going through textbook" ✅ Relevant

# \- Result 3: prof\_franklin\_cst.txt — unrelated review ❌ Wrong source

# 

# \*\*Query 3: "Is Natarajan a tough grader?"\*\*

# \- Result 1: prof\_natarajan\_cst.txt — "really tough grader" ✅ Directly relevant

# \- Result 2: prof\_sharma\_cst.txt — grading mention ⚠️ Loosely relevant

# 

# \## Grounded Generation

# 

# Grounding is enforced through the system prompt passed to the LLM:

# 

# > "Answer the question using ONLY the information in the provided reviews below. 

# > If the reviews do not contain enough information to answer the question, say 

# > exactly: 'I don't have enough information on that based on the available reviews.' 

# > Do not use any outside knowledge."

# 

# Retrieved chunks are injected into the prompt as context with source labels. 

# Source attribution is programmatically guaranteed — the sources list is extracted 

# from ChromaDB metadata before generation, not inferred by the LLM.

# 

# \## Example Responses

# 

# \*\*Query: "What do students say about Warren Franklin's exams?"\*\*

# > According to the reviews, Prof. Franklin's exams are "not that hard." The final 

# > has 2 parts — half online and half in-class. A review from 2008 notes he gives 

# > hints in class saying "you will see this again" when planning exam content.

# > Sources: prof\_franklin\_cst.txt, prof\_sharma\_cst.txt, prof\_belich\_cst.txt

# 

# \*\*Query: "What is Sergio Belich's teaching style like?"\*\*

# > Belich's teaching style involves going through the textbook during lectures. 

# > One student found this made it "tough to actually learn anything," while another 

# > described his lectures as "pretty solid." Both agree exams are based on homework.

# > Sources: prof\_belich\_cst.txt, prof\_franklin\_cst.txt, prof\_kalia\_cst.txt

# 

# \*\*Out-of-scope query: "What is the best dining hall at City Tech?"\*\*

# > I don't have enough information on that based on the available reviews.

# 

# \## Query Interface

# 

# Built with Gradio. Two input/output fields:

# \- \*\*Input:\*\* Text box for plain-language question

# \- \*\*Output:\*\* Answer box + Sources box showing which documents were retrieved

# 

# Run with: `python app.py` then open http://localhost:7860

# 

# \## Evaluation Report

# 

# | # | Question | Expected | System Response | Accuracy |

# |---|----------|----------|-----------------|----------|

# | 1 | What do students say about Warren Franklin's exams? | Exam format, difficulty, curve info | Correct — not hard, 2-part final, hints in class | ✅ Accurate |

# | 2 | Is Deodat Sharma recommended for CST students? | Positive recommendation with caveats | Correct — "awesome professor," must work hard | ✅ Accurate |

# | 3 | What is Sergio Belich's teaching style like? | Textbook-based, mixed reviews | Correct — balanced view, textbook-heavy confirmed | ✅ Accurate |

# | 4 | How does Nithya Natarajan grade assignments? | Tough grader, exam-focused | Partially correct — tough grader confirmed but wrong sources cited | ⚠️ Partially Accurate |

# | 5 | What do students say about Suman Kalia's workload? | Workload details from Kalia reviews | Failed — system said no information available | ❌ Inaccurate |

# 

# \## Failure Case

# 

# \*\*Question 5 — Suman Kalia's workload\*\* is the primary failure case.

# 

# The system returned "I don't have enough information" despite `prof\_kalia\_cst.txt` 

# containing relevant reviews. The root cause is a retrieval failure: the query 

# embedding for "Suman Kalia's workload" did not match Kalia's review chunks 

# closely enough, and ChromaDB returned chunks from Sharma and Natarajan instead.

# 

# This likely occurred because Kalia's reviews (76 lines, fewest content after 

# filtering) used different vocabulary to describe workload — words like "easy," 

# "manageable," and "not much work" rather than "workload" explicitly. The embedding 

# model matched the semantic concept of "workload" to other professors' reviews 

# that used the word more directly.

# 

# \*\*Fix in a production system:\*\* Add professor name as a metadata filter so 

# queries mentioning a specific professor always retrieve from that professor's 

# document first.

# 

# \## Spec Reflection

# 

# \*\*Where the spec helped:\*\* Writing the chunking strategy section before coding 

# forced a decision about chunk size that shaped the entire pipeline. Starting with 

# 400-character chunks and discovering they were too small during testing validated 

# the spec's prediction that chunk size directly affects retrieval quality.

# 

# \*\*Where implementation diverged:\*\* The spec anticipated 150–300 chunks from 55 

# documents. The actual count was 55 chunks — far fewer than expected. This happened 

# because the filtering step removed metadata-only chunks aggressively. In hindsight, 

# the chunk size should have been smaller (300 characters) to produce more granular 

# chunks per review.

# 

# \## AI Usage

# 

# \*\*Instance 1 — Chunking pipeline:\*\* I provided the planning.md chunking strategy 

# section and asked Claude to implement chunk.py using RecursiveCharacterTextSplitter. 

# The generated code used the wrong import path (langchain.text\_splitter instead of 

# langchain\_text\_splitters). I diagnosed the ModuleNotFoundError, installed the 

# correct package, and updated the import manually.

# 

# \*\*Instance 2 — Grounding prompt:\*\* I asked Claude to write the system prompt for 

# grounded generation. The initial version said "try to use only the provided context" 

# — I overrode this to "ONLY the information in the provided reviews" and added the 

# explicit refusal instruction to make grounding stricter.

