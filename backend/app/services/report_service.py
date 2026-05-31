from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.services.embedding_service import generate_embeddings
from app.services.similarity_service import compute_similarity
from app.utils.file_utils import list_session_files, read_file


def generate_pdf_report(session_id: str) -> bytes:
    """Builds a simple PDF report for an uploaded analysis session."""
    files = list_session_files(session_id)

    if not files:
        raise ValueError(f"Session '{session_id}' not found or contains no files.")

    if len(files) < 2:
        raise ValueError("Session must contain at least 2 files to export a report.")

    filenames = [file.name for file in files]
    snippets = [read_file(file) for file in files]
    embeddings = generate_embeddings(snippets)
    pairs = compute_similarity(filenames, embeddings, snippets)
    highest_score = max((pair["score"] for pair in pairs), default=0)

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Code Plagiarism Detector Report", styles["Title"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(f"<b>Session ID:</b> {session_id}", styles["Normal"]))
    story.append(
        Paragraph(
            f"<b>Analysis date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        )
    )
    story.append(Paragraph(f"<b>Files analyzed:</b> {len(filenames)}", styles["Normal"]))
    story.append(
        Paragraph(
            f"<b>Highest similarity detected:</b> {(highest_score * 100):.1f}%",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 18))

    story.append(Paragraph("Files Analyzed", styles["Heading2"]))
    file_rows = [[Paragraph("Filename", styles["Normal"])]]
    file_rows.extend([[Paragraph(filename, styles["Normal"])] for filename in filenames])
    file_table = Table(file_rows, colWidths=[500])
    file_table.setStyle(_basic_table_style())
    story.append(file_table)
    story.append(Spacer(1, 18))

    story.append(Paragraph("Similarity Pairs", styles["Heading2"]))
    pair_rows = [[
        Paragraph("File 1", styles["Normal"]),
        Paragraph("File 2", styles["Normal"]),
        Paragraph("Score", styles["Normal"]),
        Paragraph("Risk", styles["Normal"]),
    ]]

    for pair in pairs:
        pair_rows.append([
            Paragraph(pair["file1"], styles["Normal"]),
            Paragraph(pair["file2"], styles["Normal"]),
            Paragraph(f"{(pair['score'] * 100):.1f}%", styles["Normal"]),
            Paragraph(pair["level"].upper(), styles["Normal"]),
        ])

    pair_table = Table(pair_rows, colWidths=[180, 180, 70, 70], repeatRows=1)
    pair_table.setStyle(_basic_table_style())
    story.append(pair_table)

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _basic_table_style() -> TableStyle:
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ])
