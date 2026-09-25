"""ArticleLens NLP Studio - an interactive News Article NLP analysis application.

Run with:
    streamlit run main.py
"""

from collections import Counter
import json
import re
import string
from typing import Any

import nltk
import spacy
import streamlit as st
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize


st.set_page_config(page_title="NLP Studio", page_icon="📰", layout="wide")

SAMPLE_ARTICLE = """The city council approved a new solar-energy programme on Tuesday.
Officials said the project will install solar panels on public buildings over the
next two years. Supporters expect the programme to reduce electricity costs and
create local jobs, while critics requested clearer information about funding."""

CATEGORY_KEYWORDS = {
    "Business": {"market", "company", "stock", "economy", "profit", "trade", "bank"},
    "Environment": {"climate", "solar", "energy", "environment", "carbon", "weather", "electricity"},
    "Politics": {"government", "election", "minister", "parliament", "policy", "council", "vote"},
    "Sports": {"match", "team", "player", "coach", "tournament", "goal", "league"},
    "Technology": {"technology", "software", "ai", "device", "internet", "digital", "cyber"},
    "Health": {"health", "hospital", "doctor", "disease", "patient", "medical", "vaccine"},
}


def download_nltk_resources() -> None:
    """Fetch the small NLTK language resources used by this app if missing."""
    for resource in (
        "punkt_tab",
        "stopwords",
        "wordnet",
        "omw-1.4",
        "averaged_perceptron_tagger_eng",
        "maxent_ne_chunker_tab",
        "words",
    ):
        nltk.download(resource, quiet=True)


@st.cache_resource(show_spinner="Preparing NLP resources...")
def prepare_nltk() -> set[str]:
    """Download resources once per Streamlit server and return English stop words."""
    download_nltk_resources()
    return set(stopwords.words("english"))


@st.cache_resource
def load_spacy_model() -> Any | None:
    """Load spaCy's English pipeline; keep the NLTK app usable if it is absent."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return None


def wordnet_pos(treebank_tag: str) -> str:
    """Map a Penn Treebank tag to the tag format expected by WordNet."""
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    if treebank_tag.startswith("V"):
        return wordnet.VERB
    if treebank_tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN


def analyse_text(article: str, stop_words: set[str]) -> dict[str, Any]:
    """Run the complete preprocessing pipeline and return every stage."""
    lowercase = article.lower()
    punctuation_removed = lowercase.translate(str.maketrans("", "", string.punctuation))
    special_characters_removed = re.sub(r"[^a-z\s]", " ", punctuation_removed)
    cleaned_text = re.sub(r"\s+", " ", special_characters_removed).strip()

    tokens = word_tokenize(cleaned_text)
    tokens_without_stopwords = [token for token in tokens if token not in stop_words]

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens_without_stopwords]
    tagged_tokens = nltk.pos_tag(tokens_without_stopwords)
    lemmatized_tokens = [
        lemmatizer.lemmatize(token, wordnet_pos(tag)) for token, tag in tagged_tokens
    ]
    summary_sentences = create_extractive_summary(article, stop_words)
    named_entities = extract_named_entities(article)
    category, category_keywords = predict_category(lemmatized_tokens)
    spacy_results = analyse_with_spacy(article)

    return {
        "statistics": {
            "Characters": len(article),
            "Words": len(re.findall(r"\b\w+\b", article)),
            "Sentences": len(sent_tokenize(article)),
            "Tokens after cleaning": len(tokens),
            "Tokens after stopword removal": len(tokens_without_stopwords),
        },
        "lowercase": lowercase,
        "punctuation_removed": punctuation_removed,
        "special_characters_removed": special_characters_removed,
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "tokens_without_stopwords": tokens_without_stopwords,
        "stemmed_tokens": stemmed_tokens,
        "lemmatized_tokens": lemmatized_tokens,
        "frequencies": Counter(lemmatized_tokens),
        "summary_sentences": summary_sentences,
        "named_entities": named_entities,
        "predicted_category": category,
        "category_keywords": category_keywords,
        "spacy_results": spacy_results,
    }


def preprocess_for_analysis(text: str, stop_words: set[str]) -> tuple[list[str], list[str], list[str]]:
    """Apply the shared NLP preprocessing steps used by analysis features."""
    raw_tokens = word_tokenize(text.lower())
    words = [token for token in raw_tokens if re.fullmatch(r"[a-z]+", token)]
    cleaned_tokens = [token for token in words if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = nltk.pos_tag(cleaned_tokens)
    lemmatized_tokens = [
        lemmatizer.lemmatize(token, wordnet_pos(tag)) for token, tag in tagged_tokens
    ]
    return raw_tokens, cleaned_tokens, lemmatized_tokens


def create_extractive_summary(article: str, stop_words: set[str], sentence_limit: int = 3) -> list[str]:
    """Select important article sentences using frequency-weighted NLP scoring."""
    sentences = sent_tokenize(article)
    _, _, article_terms = preprocess_for_analysis(article, stop_words)
    frequencies = Counter(article_terms)
    scored_sentences: list[tuple[float, int, str]] = []

    for position, sentence in enumerate(sentences):
        _, _, sentence_terms = preprocess_for_analysis(sentence, stop_words)
        if sentence_terms:
            score = sum(frequencies[term] for term in sentence_terms) / len(sentence_terms)
            scored_sentences.append((score, position, sentence))

    top_sentences = sorted(scored_sentences, reverse=True)[:sentence_limit]
    # Restore article order so the summary reads naturally.
    return [sentence for _, _, sentence in sorted(top_sentences, key=lambda item: item[1])]


def extract_named_entities(article: str) -> dict[str, list[str]]:
    """Extract people, organizations, and locations with NLTK's NE chunker."""
    entities: dict[str, list[str]] = {"People": [], "Organizations": [], "Locations": [], "Dates": []}
    entity_labels = {"PERSON": "People", "ORGANIZATION": "Organizations", "GPE": "Locations", "LOCATION": "Locations"}
    tagged_words = nltk.pos_tag(word_tokenize(article))
    for chunk in nltk.ne_chunk(tagged_words):
        if hasattr(chunk, "label") and chunk.label() in entity_labels:
            name = " ".join(word for word, _ in chunk.leaves())
            group = entity_labels[chunk.label()]
            if name not in entities[group]:
                entities[group].append(name)

    date_pattern = r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December)\b"
    entities["Dates"] = re.findall(date_pattern, article, flags=re.IGNORECASE)
    return entities


def predict_category(lemmatized_tokens: list[str]) -> tuple[str, list[str]]:
    """Predict a news category using transparent keyword scores."""
    terms = set(lemmatized_tokens)
    matches = {
        category: sorted(terms.intersection(keywords))
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    category = max(matches, key=lambda name: len(matches[name]))
    if not matches[category]:
        return "General news", []
    return category, matches[category]


def analyse_with_spacy(article: str) -> dict[str, Any]:
    """Create a spaCy version of the tokenization and lemmatization results."""
    nlp = load_spacy_model()
    if nlp is None:
        return {"available": False}

    doc = nlp(article)
    raw_tokens = [token.text for token in doc]
    cleaned_tokens = [
        token.text.lower()
        for token in doc
        if token.is_alpha and not token.is_stop
    ]
    lemmatized_tokens = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and not token.is_stop
    ]
    entities = [f"{entity.text} ({entity.label_})" for entity in doc.ents]
    return {
        "available": True,
        "raw_tokens": raw_tokens,
        "cleaned_tokens": cleaned_tokens,
        "lemmatized_tokens": lemmatized_tokens,
        "entities": entities,
    }


def token_chips(tokens: list[str], limit: int = 80) -> None:
    """Render a compact, readable preview of a token list."""
    preview = tokens[:limit]
    st.code("  |  ".join(preview) if preview else "No tokens", language=None)
    if len(tokens) > limit:
        st.caption(f"Showing {limit} of {len(tokens)} tokens.")


def show_pipeline(results: dict[str, Any]) -> None:
    """Display all transformations in the requested NLP workflow."""
    st.subheader("1. Text statistics")
    metric_columns = st.columns(5)
    for column, (label, value) in zip(metric_columns, results["statistics"].items()):
        column.metric(label, value)

    st.subheader("2. Text cleaning")
    cleaning_tabs = st.tabs(
        ["Lowercase", "Punctuation removed", "Special characters removed", "Final cleaned text"]
    )
    for tab, key in zip(
        cleaning_tabs,
        ["lowercase", "punctuation_removed", "special_characters_removed", "cleaned_text"],
    ):
        with tab:
            st.write(results[key])

    st.subheader("3. Tokenization and the  stop-words removal")
    token_column, stopword_column = st.columns(2)
    with token_column:
        st.markdown(f"**Tokens ({len(results['tokens'])})**")
        token_chips(results["tokens"])
    with stopword_column:
        st.markdown(f"**Meaningful tokens ({len(results['tokens_without_stopwords'])})**")
        token_chips(results["tokens_without_stopwords"])

    st.subheader("4. Stemming vs. lemmatization")
    stem_column, lemma_column = st.columns(2)
    with stem_column:
        st.markdown("**Stemmed tokens** — shortened word roots")
        token_chips(results["stemmed_tokens"])
    with lemma_column:
        st.markdown("**Lemmatized tokens** — dictionary base forms")
        token_chips(results["lemmatized_tokens"])

    st.subheader("5. Word-frequency analysis")
    top_words = results["frequencies"].most_common(10)
    if top_words:
        st.bar_chart({"Frequency": {word: count for word, count in top_words}})
        st.caption("Top 10 lemmatized words in the article")
    else:
        st.info("Enter more alphabetic text to create a frequency chart.")


def show_advanced_analysis(results: dict[str, Any]) -> None:
    """Display the higher-level analysis features built from processed tokens."""
    st.subheader("6. Article summary and category")
    summary_column, category_column = st.columns([2, 1])
    with summary_column:
        st.markdown("**Extractive summary**")
        if results["summary_sentences"]:
            st.write(" ".join(results["summary_sentences"]))
        else:
            st.info("A summary needs at least one complete sentence.")
    with category_column:
        st.metric("Predicted category", results["predicted_category"])
        matched = results["category_keywords"]
        st.caption(f"Matched keywords: {', '.join(matched) if matched else 'No category keywords'}")
        st.caption("Category prediction is rule-based and transparent for learning.")

    st.subheader("7. Named Entity Recognition")
    st.caption("Entities are detected with NLTK; dates are also identified with a date-name pattern.")
    entity_columns = st.columns(4)
    for column, (entity_type, values) in zip(entity_columns, results["named_entities"].items()):
        with column:
            st.markdown(f"**{entity_type}**")
            if values:
                for value in values:
                    st.write(f"• {value}")
            else:
                st.caption("None found")


def show_spacy_comparison(results: dict[str, Any]) -> None:
    """Show spaCy's processing beside the existing NLTK pipeline."""
    st.subheader("8. spaCy preprocessing comparison")
    spacy_results = results["spacy_results"]
    if not spacy_results["available"]:
        st.warning(
            "spaCy is installed, but its English model is not available. Run "
            "`py -m spacy download en_core_web_sm` once, then restart the app."
        )
        return

    raw_column, cleaned_column, lemma_column = st.columns(3)
    with raw_column:
        st.markdown(f"**spaCy raw tokens ({len(spacy_results['raw_tokens'])})**")
        token_chips(spacy_results["raw_tokens"])
    with cleaned_column:
        st.markdown(f"**spaCy tokens without stop words ({len(spacy_results['cleaned_tokens'])})**")
        token_chips(spacy_results["cleaned_tokens"])
    with lemma_column:
        st.markdown("**spaCy lemmas**")
        token_chips(spacy_results["lemmatized_tokens"])

    st.markdown("**spaCy named entities**")
    st.write(", ".join(spacy_results["entities"]) if spacy_results["entities"] else "No entities detected."
    )


def main() -> None:
    st.markdown(
        """<style>
        .block-container {max-width: 1150px; padding-top: 2rem;}
        .hero {padding: 1.5rem; border-radius: 16px; color: white;
               background: linear-gradient(120deg, #0f172a, #0369a1); margin-bottom: 1rem;}
        </style>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="hero"><h1>📰NLP Studio</h1>
        <p>Explore how NLP cleans, summarizes, and analyses a news article.</p></div>""",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("How it works")
        st.caption("Raw text → statistics → cleaning → tokenization → stop-word removal → stemming and lemmatization → analysis")
        if st.button("Load sample article"):
            st.session_state.article_text = SAMPLE_ARTICLE
        uploaded_file = st.file_uploader("Or upload a .txt article", type=["txt"])
        if uploaded_file is not None:
            st.session_state.article_text = uploaded_file.getvalue().decode("utf-8", errors="replace")

    if "article_text" not in st.session_state:
        st.session_state.article_text = SAMPLE_ARTICLE

    article = st.text_area(
        "Paste a news article or paragraph",
        key="article_text",
        height=230,
        placeholder="Paste your news article here...",
    )

    if st.button("Analyse article", type="primary", use_container_width=True):
        if not article.strip():
            st.warning("Please paste a news article or paragraph before analysing it.")
            return
        try:
            stop_words = prepare_nltk()
            results = analyse_text(article, stop_words)
        except LookupError as error:
            st.error(f"NLTK resource setup failed: {error}")
            return

        st.session_state.analysed_article = article
        st.session_state.analysis_results = results

    if st.session_state.get("analysed_article") == article:
        results = st.session_state.analysis_results
        stop_words = prepare_nltk()
        show_pipeline(results)
        show_advanced_analysis(results)
        show_spacy_comparison(results)
        export_data = {
            key: value
            for key, value in results.items()
            if key != "frequencies"
        }
        export_data["word_frequencies"] = dict(results["frequencies"])
        st.download_button(
            "Download analysis as JSON",
            data=json.dumps(export_data, indent=2),
            file_name="articlelens_analysis.json",
            mime="application/json",
        )

    st.divider()
    st.caption(
        "Why this matters: cleaned and normalized text improves traditional ML features, "
        "search indexes, topic models, and review/feedback analysis. LLMs use their own "
        "subword tokenizers, but preprocessing is still valuable for data quality and retrieval."
    )


if __name__ == "__main__":
    main()
