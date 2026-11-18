import { EditorView, basicSetup } from "codemirror";
import { markdown } from "@codemirror/lang-markdown";

import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";

import {
    HighlightStyle,
    StreamLanguage,
    syntaxHighlighting,
} from "@codemirror/language";
import { csharp } from "@codemirror/legacy-modes/mode/clike";
import { shell } from "@codemirror/legacy-modes/mode/shell";
import { tags } from "@lezer/highlight";


import "../css/markdown-editor.css";

const shellLanguage = StreamLanguage.define(shell);
const csharpLanguage = StreamLanguage.define(csharp);

const editorHighlighting = syntaxHighlighting(
    HighlightStyle.define([
        { tag: tags.keyword, color: "#ff7ab2", fontWeight: "700" },
        { tag: tags.operator, color: "#f78c6c" },
        { tag: tags.string, color: "#c3e88d" },
        { tag: tags.number, color: "#f78c6c" },
        { tag: tags.bool, color: "#ff9cac", fontWeight: "700" },
        { tag: tags.function(tags.variableName), color: "#82aaff" },
        { tag: tags.variableName, color: "#f8f8f2" },
        { tag: [tags.typeName, tags.className], color: "#80cbc4" },
        { tag: tags.comment, color: "#8fa1b3", fontStyle: "italic" },
        { tag: tags.heading, color: "#ffd166", fontWeight: "700" },
        { tag: tags.link, color: "#7dd3fc", textDecoration: "underline" },
    ])
);

const codeLanguages = (info) => {
    const language = info.trim().toLowerCase();

    const languages = {
        python: python().language,
        py: python().language,
        bash: shellLanguage,
        sh: shellLanguage,
        shell: shellLanguage,
        javascript: javascript().language,
        js: javascript().language,
        csharp: csharpLanguage,
        cs: csharpLanguage,
        "c#": csharpLanguage,
    };

    return languages[language] ?? null;
};

let previewRequest;

function updateMarkdownPreview(content) {
    const preview = document.querySelector(".markdown-preview");
    const previewUrl = window.MARKDOWN_PREVIEW_URL;

    if (!preview || !previewUrl) {
        return;
    }

    window.clearTimeout(previewRequest);
    previewRequest = window.setTimeout(async () => {
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');

        try {
            const response = await fetch(previewUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "X-CSRFToken": csrfInput?.value ?? "",
                },
                body: new URLSearchParams({ content }),
            });

            if (!response.ok) {
                throw new Error("Não foi possível gerar a prévia.");
            }

            const data = await response.json();
            preview.innerHTML = data.html || '<p class="markdown-preview-empty">A prévia aparecerá aqui enquanto você escreve.</p>';
        } catch (error) {
            preview.innerHTML = `<p class="markdown-preview-empty">${error.message}</p>`;
        }
    }, 180);
}

function setupMarkdownPreview(textarea, editor) {
    const workbench = document.querySelector(".markdown-workbench");
    const modeButtons = document.querySelectorAll("[data-editor-mode]");

    modeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const mode = button.dataset.editorMode;
            workbench.dataset.mode = mode;
            modeButtons.forEach((item) => item.classList.toggle("active", item === button));
            editor.requestMeasure();

            if (mode !== "edit") {
                updateMarkdownPreview(editor.state.doc.toString());
            }
        });
    });

    textarea.form?.addEventListener("submit", () => {
        textarea.value = editor.state.doc.toString();
    });

    updateMarkdownPreview(editor.state.doc.toString());
}

function initializeMarkdownEditor() {
    const textarea = document.querySelector(
        'textarea[name="content"]'
    );

    if (!textarea || textarea.dataset.codemirrorInitialized) {
        return;
    }

    const container = document.createElement("div");
    container.className = "markdown-editor";

    textarea.parentNode.insertBefore(container, textarea);

    const editor = new EditorView({
        doc: textarea.value,
        extensions: [
            basicSetup,
            markdown({codeLanguages,}),
            editorHighlighting,
            EditorView.lineWrapping,
            EditorView.updateListener.of((update) => {
                if (update.docChanged) {
                    textarea.value = update.state.doc.toString();
                    updateMarkdownPreview(update.state.doc.toString());
                }
            }),
        ],
        parent: container,
    });

    setupMarkdownPreview(textarea, editor);

    textarea.dataset.codemirrorInitialized = "true";
    textarea.style.display = "none";
}

if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        initializeMarkdownEditor
    );
} else {
    initializeMarkdownEditor();
}
