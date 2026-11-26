const createPostForm = document.querySelector(".create-post-form");

if (createPostForm) {
    window.MARKDOWN_PREVIEW_URL = createPostForm.dataset.markdownPreviewUrl;

    const imageInput = createPostForm.querySelector("[data-image-preview] ~ input[type='file']")
        ?? createPostForm.querySelector("input[type='file'][name='image']");
    const imagePreview = createPostForm.querySelector("[data-image-preview]");
    const imagePlaceholder = createPostForm.querySelector("[data-image-placeholder]");

    imageInput?.addEventListener("change", () => {
        const [selectedImage] = imageInput.files;
        if (!selectedImage || !imagePreview || !imagePlaceholder) return;

        imagePreview.src = URL.createObjectURL(selectedImage);
        imagePreview.classList.remove("is-empty");
        imagePlaceholder.hidden = true;
        imagePlaceholder.classList.add("is-hidden");
    });
}
