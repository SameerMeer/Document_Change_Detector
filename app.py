import streamlit as st

from change_detector import compare_documents


st.set_page_config(
    page_title="Document Change Detector",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Document Change Detector")

st.write(
    "Upload two versions of a PDF to detect added, removed, "
    "modified, and unchanged sections."
)


# --------------------------------
# PDF Upload
# --------------------------------

col1, col2 = st.columns(2)

with col1:
    old_pdf = st.file_uploader(
        "📕 Upload OLD PDF",
        type=["pdf"]
    )

with col2:
    new_pdf = st.file_uploader(
        "📗 Upload NEW PDF",
        type=["pdf"]
    )


# --------------------------------
# Compare Button
# --------------------------------

if old_pdf and new_pdf:

    if st.button(
        "🔍 Compare Documents",
        type="primary"
    ):

        with st.spinner(
            "Analyzing documents... This may take a moment."
        ):

            # Save uploaded files temporarily
            with open("old_uploaded.pdf", "wb") as file:
                file.write(old_pdf.getbuffer())

            with open("new_uploaded.pdf", "wb") as file:
                file.write(new_pdf.getbuffer())


            # Run comparison
            results = compare_documents(
                "old_uploaded.pdf",
                "new_uploaded.pdf"
            )


        st.success("Document comparison completed!")


        # --------------------------------
        # Summary
        # --------------------------------

        modified = sum(
            1 for r in results
            if r["status"] == "MODIFIED"
        )

        unchanged = sum(
            1 for r in results
            if r["status"] == "UNCHANGED"
        )

        added = sum(
            1 for r in results
            if r["status"] == "ADDED"
        )

        removed = sum(
            1 for r in results
            if r["status"] == "REMOVED"
        )


        st.subheader("📊 Comparison Summary")


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Modified",
                modified
            )

        with col2:
            st.metric(
                "Unchanged",
                unchanged
            )

        with col3:
            st.metric(
                "Added",
                added
            )

        with col4:
            st.metric(
                "Removed",
                removed
            )


        st.divider()


        # --------------------------------
        # Section Results
        # --------------------------------

        st.subheader("📋 Section-by-Section Changes")


        for result in results:

            status = result["status"]

            section = result["section"]


            # ----------------------------
            # Unchanged
            # ----------------------------

            if status == "UNCHANGED":

                with st.expander(
                    f"🟢 {section} — UNCHANGED"
                ):

                    st.write(
                        f"Old Page: {result['old_page']}"
                    )

                    st.write(
                        f"New Page: {result['new_page']}"
                    )

                    st.write(
                        f"Similarity: "
                        f"{result['similarity']:.4f}"
                    )


            # ----------------------------
            # Modified
            # ----------------------------

            elif status == "MODIFIED":

                with st.expander(
                    f"🟡 {section} — MODIFIED",
                    expanded=True
                ):

                    st.write(
                        f"Old Page: {result['old_page']}"
                    )

                    st.write(
                        f"New Page: {result['new_page']}"
                    )

                    st.write(
                        f"Semantic Similarity: "
                        f"{result['similarity']:.4f}"
                    )


                    st.markdown("### 📕 Old Text")

                    st.info(
                        result["old_text"]
                    )


                    st.markdown("### 📗 New Text")

                    st.success(
                        result["new_text"]
                    )


                    st.markdown("### ❌ Removed")

                    if result["removed"]:
                        st.write(
                            " ".join(
                                result["removed"]
                            )
                        )
                    else:
                        st.write("None")


                    st.markdown("### ➕ Added")

                    if result["added"]:
                        st.write(
                            " ".join(
                                result["added"]
                            )
                        )
                    else:
                        st.write("None")


                    st.markdown("### 🤖 AI Explanation")

                    if result["explanation"]:
                        st.write(
                            result["explanation"]
                        )


            # ----------------------------
            # Added
            # ----------------------------

            elif status == "ADDED":

                with st.expander(
                    f"🔵 {section} — ADDED",
                    expanded=True
                ):

                    st.write(
                        f"New Page: {result['new_page']}"
                    )

                    st.write(
                        f"Similarity: "
                        f"{result['similarity']:.4f}"
                    )

                    st.markdown("### 📗 New Section")

                    st.success(
                        result["new_text"]
                    )


            # ----------------------------
            # Removed
            # ----------------------------

            elif status == "REMOVED":

                with st.expander(
                    f"🔴 {section} — REMOVED",
                    expanded=True
                ):

                    st.write(
                        f"Old Page: {result['old_page']}"
                    )

                    st.write(
                        f"Similarity: "
                        f"{result['similarity']:.4f}"
                    )

                    st.markdown("### 📕 Removed Section")

                    st.error(
                        result["old_text"]
                    )