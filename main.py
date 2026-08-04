from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question


load_dotenv()

def run_pipeline(source: str, language: str = "english", on_step=None) -> dict:
    """
    Runs the full AI Video Assistant pipeline.

    on_step: optional callback(key: str, state: str) invoked before/after each
    stage with state in {"active", "done"}. Used by app.py to drive the UI's
    live status sidebar without duplicating this logic. CLI usage is
    unaffected since on_step defaults to None.
    """
    def _notify(key, state):
        if on_step:
            on_step(key, state)

    print("starting AI Video Assistant")

    _notify("audio", "active")
    chunks = process_input(source)
    _notify("audio", "done")

    _notify("transcript", "active")
    transcript = transcribe_all(chunks, language)
    print(f"raw transcription (first 300 characters ) {transcript[:300]}")
    _notify("transcript", "done")

    _notify("title", "active")
    title = generate_title(transcript)
    _notify("title", "done")

    _notify("summary", "active")
    summary = summarize(transcript)
    _notify("summary", "done")

    _notify("extract", "active")
    action_item = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    _notify("extract", "done")

    _notify("rag", "active")
    rag_chain = build_rag_chain(transcript)
    _notify("rag", "done")

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

if __name__ == "__main__":
    # CLI entry point
    source = input("Enter YouTube URL or local file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "=" * 60)
    print(f"📌 Title: {result['title']}")
    print(f"\n📋 Summary:\n{result['summary']}")
    print(f"\n✅ Action Items:\n{result['action_items']}")
    print(f"\n🔑 Key Decisions:\n{result['key_decisions']}")
    print(f"\n❓ Open Questions:\n{result['open_questions']}")
    print("=" * 60)

    # Phase 2 — Chat with your meeting via RAG
    print("\n💬 Chat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\n🤖 Assistant: {answer}\n")