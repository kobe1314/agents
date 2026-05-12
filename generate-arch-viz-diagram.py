#!/usr/bin/env python3
"""
Generate an Excalidraw architecture diagram for the Arch-Viz system.
Usage: python3 generate-arch-viz-diagram.py
Output: arch-viz-architecture.excalidraw

Design based on:
  - 8 agents (plan, build, reviewer, debugger, test, docs, refactor, architect)
  - 9 skills installed in .agents/skills/
  - 1 MCP service (github)
  - 3-layer architecture: CLI → Collectors → Data Model → Renderers
"""

import json
import time

# ─── ID Generator ────────────────────────────────────────────────────────

_counter = 0


def eid():
    """Generate globally unique element IDs."""
    global _counter
    _counter += 1
    return f"el-{_counter:05d}"


# ─── Validated Element Builders ──────────────────────────────────────────
# Critical: all builders follow Excalidraw JSON schema constraints:
#   - fontFamily ∈ {1, 2, 3}   (No 5!)
#   - rectangle roundness = {"type": 3}
#   - arrow roundness     = {"type": 2}
#   - text roundness      = null
#   - NO "text" field on rectangles
#   - NO containerId / boundElements bindings
#   - autoResize = false


def rect(x, y, w, h, bg="#d0ebff", stroke="#1e1e1e", rounded=True):
    """Rectangle. NO text/boundElements property."""
    return {
        "type": "rectangle",
        "version": 1,
        "id": eid(),
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": {"type": 3} if rounded else None,
        "seed": int(time.time() * 100000 + _counter) % 2**31,
        "isDeleted": False,
        "boundElements": None,
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
        "frameId": None,
    }


def txt(x, y, w, h, text, size=16, color="#1e1e1e", align="center", bold=False):
    """Standalone text element. Never uses containerId or boundElements."""
    return {
        "type": "text",
        "version": 1,
        "id": eid(),
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2 if bold else 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "roundness": None,
        "seed": int(time.time() * 100000 + _counter + 1000) % 2**31,
        "isDeleted": False,
        "boundElements": None,
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": size,
        "fontFamily": 2,  # 正楷
        "textAlign": align,
        "verticalAlign": "middle",
        "containerId": None,
        "autoResize": False,
        "lineHeight": 1.2,
        "baseline": y + h // 2 + size // 3,
        "frameId": None,
        "originalText": text,
    }


def arrow(x1, y1, x2, y2, color="#495057", style="solid", label=""):
    """Arrow with roundness type 2. May include optional label text."""
    elements = []
    a = {
        "type": "arrow",
        "version": 1,
        "id": eid(),
        "x": min(x1, x2),
        "y": min(y1, y2),
        "width": abs(x2 - x1),
        "height": abs(y2 - y1),
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": style,
        "roughness": 0,
        "opacity": 80,
        "groupIds": [],
        "roundness": {"type": 2},
        "seed": int(time.time() * 100000 + _counter + 2000) % 2**31,
        "isDeleted": False,
        "boundElements": None,
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "frameId": None,
    }
    elements.append(a)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        tw = len(label) * 7 + 8
        th = 16
        elements.append(
            txt(mx - tw // 2, my - th - 2, tw, th, label, size=10, color=color)
        )
    return elements


# ─── Text-in-Box Helpers ────────────────────────────────────────────────
# Use these instead of manual txt() calls inside rect() —
# they calculate proper vertical centering so text doesn't
# appear at the top of the box.


def center_in_box(
    x, y, w, h, text, size=16, color="#1e1e1e", bold=False, align="center"
):
    """Single-line text vertically centered inside a box at (x,y,w,h).
    Returns one text element.
    """
    text_h = size + 4  # enough for one line
    ty = y + (h - text_h) // 2
    return txt(x, ty, w, text_h, text, size=size, color=color, bold=bold, align=align)


def lines_in_box(x, y, w, h, lines, sizes, colors=None, align="left", pad_x=8):
    """Multiple lines evenly spaced and vertically centered inside a box.

    Args:
        x, y, w, h: box dimensions
        lines: list of text strings
        sizes: list of font sizes (one per line)
        colors: optional list of colors (defaults to dark text)
        align: text alignment
        pad_x: horizontal padding

    Returns: list of text elements (rect not included)
    """
    els = []
    n = len(lines)
    if colors is None:
        colors = ["#1e1e1e"] * n
    if len(sizes) != n:
        sizes = [sizes[0]] * n  # replicate if single size given

    line_heights = [s + 4 for s in sizes]
    total_text_h = sum(line_heights)
    # Distribute remaining space evenly above first and between lines
    gap = (h - total_text_h) / (n + 1)
    cy = y + gap
    for i in range(n):
        lh = line_heights[i]
        bold = i == 0  # first line bold
        els.append(
            txt(
                x + pad_x,
                cy,
                w - 2 * pad_x,
                lh,
                lines[i],
                size=sizes[i],
                color=colors[i],
                bold=bold,
                align=align,
            )
        )
        cy += lh + gap
    return els


# ─── Layout ──────────────────────────────────────────────────────────────
# Canvas: 1280 x 900
# Rows:    CLI (y=90) | Engine (y=200-510) | Sources (y=550-630) | Output (y=690-760)

CW, CH = 1280, 900
E = []  # elements array

# ═══════════════════════════════════════════════════════════════════════════
# 0. TITLE
# ═══════════════════════════════════════════════════════════════════════════
E.append(
    txt(
        340,
        15,
        600,
        36,
        "🧠  Arch-Viz Architecture  ·  架构可视化系统",
        size=24,
        bold=True,
    )
)
E.append(
    txt(
        420,
        48,
        440,
        18,
        "Agent Topology  /  Skill Dependencies  /  MCP Status",
        size=12,
        color="#868e96",
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 1. CLI LAYER  (y=90-160)
# ═══════════════════════════════════════════════════════════════════════════
L1_Y = 90
L1_H = 70
# Background
E.append(rect(40, L1_Y, 1190, L1_H, "#f1f3f5", "#d0d0d0"))
E.append(
    center_in_box(15, L1_Y, 60, L1_H, "CLI", size=11, color="#868e96", align="center")
)

# /arch-viz slash command  (box 220x40)
bx, by, bw, bh = 180, L1_Y + 15, 220, 40
E.append(rect(bx, by, bw, bh, "#d0ebff", "#1e1e1e"))
E.append(center_in_box(bx, by, bw, bh, "/arch-viz", size=15, bold=True))

# Arrow → meow
E.extend(arrow(400, L1_Y + 35, 470, L1_Y + 35, "#495057"))

# meow arg parser  (box 230x40, 2 lines)
bx, by, bw, bh = 470, L1_Y + 15, 230, 40
E.append(rect(bx, by, bw, bh, "#d0ebff", "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "meow ArgParser",
            "--mode  --export  --watch",
        ],
        sizes=[12, 9],
        colors=["#1e1e1e", "#495057"],
        align="center",
        pad_x=4,
    )
)

# Arrow → ink
E.extend(arrow(700, L1_Y + 35, 770, L1_Y + 35, "#495057"))

# Ink App Root  (box 290x40, 2 lines)
bx, by, bw, bh = 770, L1_Y + 15, 290, 40
E.append(rect(bx, by, bw, bh, "#d0ebff", "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "Ink  (React for Terminal)",
            "<App>  <TopologyTree>  <SkillTree>  <MCPTable>",
        ],
        sizes=[12, 9],
        colors=["#1e1e1e", "#495057"],
        align="center",
        pad_x=4,
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. CORE ENGINE  (y=200-510)
# ═══════════════════════════════════════════════════════════════════════════
L2_Y = 200
L2_H = 310
# Background
E.append(rect(40, L2_Y, 1190, L2_H, "#f8f9fa", "#d0d0d0"))
E.append(
    center_in_box(
        15, L2_Y, 60, L2_H, "Engine", size=11, color="#868e96", align="center"
    )
)

# ── 2a. COLLECTORS (x=80, w=260) ─────────────────────────────────────────
CX, CWID = 80, 260
CCOL = "#b2f2bb"

# Section header
E.append(rect(CX, L2_Y + 15, CWID, 30, "#e9ecef", "#adb5bd"))
E.append(
    center_in_box(CX, L2_Y + 15, CWID, 30, "🔍  Collectors  收集器", size=13, bold=True)
)

# AgentCollector  (box 60px tall, 3 lines)
bx, by, bw, bh = CX, L2_Y + 60, CWID, 60
E.append(rect(bx, by, bw, bh, CCOL, "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "AgentCollector",
            "opencode.json + AGENTS.md",
            "→ AgentNode[] + WorkflowEdge[]",
        ],
        sizes=[13, 9, 9],
        colors=["#1e1e1e", "#2b8a3e", "#2b8a3e"],
    )
)

# SkillCollector  (box 60px tall, 3 lines)
bx, by, bw, bh = CX, L2_Y + 130, CWID, 60
E.append(rect(bx, by, bw, bh, CCOL, "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "SkillCollector",
            ".agents/skills/*/ + skills-lock.json",
            "→ SkillNode[] + dependency edges",
        ],
        sizes=[13, 9, 9],
        colors=["#1e1e1e", "#2b8a3e", "#2b8a3e"],
    )
)

# MCPChecker  (box 60px tall, 3 lines)
bx, by, bw, bh = CX, L2_Y + 200, CWID, 60
E.append(rect(bx, by, bw, bh, CCOL, "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "MCPChecker",
            "opencode.json mcp + health check",
            "→ MCPNode[] + connection status",
        ],
        sizes=[13, 9, 9],
        colors=["#1e1e1e", "#2b8a3e", "#2b8a3e"],
    )
)

# ── 2b. DATA MODEL (x=420, w=440) ────────────────────────────────────────
MX, MWID = 420, 440
MCOL = "#ffd43b"

# Section header
E.append(rect(MX, L2_Y + 15, MWID, 30, "#e9ecef", "#adb5bd"))
E.append(
    center_in_box(
        MX,
        L2_Y + 15,
        MWID,
        30,
        "📐  Data Model & Orchestrator  数据模型与编排",
        size=13,
        bold=True,
    )
)

# TopologyGraph  (big box, 100px tall, 4 lines)
bx, by, bw, bh = MX, L2_Y + 60, MWID, 100
E.append(rect(bx, by, bw, bh, MCOL, "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "🧩  TopologyGraph",
            "nodes:  (AgentNode | SkillNode | MCPNode)[]",
            "edges:  Edge[]  |  metadata: { projectName, platform, collectedAt }",
            "types:  AgentRole | AgentModel | ToolType | MCPStatus",
        ],
        sizes=[15, 10, 10, 10],
        colors=["#1e1e1e", "#5c4a00", "#5c4a00", "#5c4a00"],
    )
)

# GraphBuilder  (box 85px tall, 4 lines)
bx, by, bw, bh = MX, L2_Y + 175, MWID, 85
E.append(rect(bx, by, bw, bh, MCOL, "#1e1e1e"))
E.extend(
    lines_in_box(
        bx,
        by,
        bw,
        bh,
        [
            "⚙️  GraphBuilder",
            "build()  →  TopologyGraph",
            "collect → validate → assemble → return",
            "orchestrates all 3 collectors concurrently",
        ],
        sizes=[15, 10, 10, 10],
        colors=["#1e1e1e", "#5c4a00", "#5c4a00", "#5c4a00"],
    )
)

# ── 2c. RENDERERS (x=940, w=260) ─────────────────────────────────────────
RX, RWID = 940, 260
RCOL = "#dabfff"

# Section header
E.append(rect(RX, L2_Y + 15, RWID, 30, "#e9ecef", "#adb5bd"))
E.append(
    center_in_box(RX, L2_Y + 15, RWID, 30, "🎨  Renderers  渲染器", size=13, bold=True)
)

# Renderer boxes (each 45px tall, single line)
renderers = [
    (L2_Y + 60, "TopologyTree  (Agent)", 13, 45),
    (L2_Y + 115, "SkillTree  (Dependencies)", 13, 45),
    (L2_Y + 170, "MCPTable  (Status)", 13, 45),
    (L2_Y + 225, "SummaryPanel  (Stats)", 11, 35),
]
for ry, label, rsize, rh in renderers:
    E.append(rect(RX, ry, RWID, rh, RCOL, "#1e1e1e"))
    E.append(center_in_box(RX, ry, RWID, rh, label, size=rsize, bold=True))

# ── Internal Arrows ──────────────────────────────────────────────────────

# Collectors → Data Model (rightward)
col_mid_y_offsets = [L2_Y + 90, L2_Y + 160, L2_Y + 230]
for cy in col_mid_y_offsets:
    E.extend(arrow(CX + CWID, cy, MX, L2_Y + 110, "#2f9e44", "dashed", "data"))

# Data Model → Renderers (rightward)
E.extend(arrow(MX + MWID, L2_Y + 110, RX, L2_Y + 82, "#7048e8", "dashed", "render"))

# ═══════════════════════════════════════════════════════════════════════════
# 3. DATA SOURCES  (y=550-630)
# ═══════════════════════════════════════════════════════════════════════════
L3_Y = 550
L3_H = 85
E.append(rect(40, L3_Y, 1190, L3_H, "#f1f3f5", "#d0d0d0"))
E.append(
    center_in_box(
        15, L3_Y, 60, L3_H, "Sources", size=11, color="#868e96", align="center"
    )
)

SCOL = "#ffc9c9"
src_data = [
    ("opencode.json", "Agent/MCP config"),
    ("AGENTS.md", "Agent table + workflows"),
    (".agents/skills/*/", "Meta + SKILL.md"),
    ("skills-lock.json", "Sourced skill tracking"),
    (".opencode/rules/*.md", "Selection rules"),
]
src_count = len(src_data)
src_gap = 1100 // src_count
src_start_x = 100

for i, (name, desc) in enumerate(src_data):
    sx = src_start_x + i * src_gap
    sw = src_gap - 15
    sh = 50
    E.append(rect(sx, L3_Y + 18, sw, sh, SCOL, "#c92a2a"))
    E.extend(
        lines_in_box(
            sx,
            L3_Y + 18,
            sw,
            sh,
            [name, desc],
            sizes=[11, 9],
            colors=["#1e1e1e", "#c92a2a"],
            pad_x=4,
        )
    )

    # Upward arrow from source to engine
    E.extend(
        arrow(
            sx + sw // 2,
            L3_Y + 18,
            sx + sw // 2,
            L2_Y + L2_H - 5,
            "#e03131",
            "dashed",
            "",
        )
    )

# ═══════════════════════════════════════════════════════════════════════════
# 4. OUTPUT  (y=690-760)
# ═══════════════════════════════════════════════════════════════════════════
L4_Y = 690
L4_H = 70
E.append(rect(40, L4_Y, 1190, L4_H, "#f1f3f5", "#d0d0d0"))
E.append(
    center_in_box(
        15, L4_Y, 60, L4_H, "Output", size=11, color="#868e96", align="center"
    )
)

OCOL = "#ffec99"

# Terminal box (340x40)
bx, by, bw, bh = 250, L4_Y + 15, 340, 40
E.append(rect(bx, by, bw, bh, OCOL, "#1e1e1e"))
E.append(
    center_in_box(
        bx, by, bw, bh, "🖥️  Terminal  (tree / table / panel)", size=13, bold=True
    )
)

# Export box (400x40)
bx, by, bw, bh = 660, L4_Y + 15, 400, 40
E.append(rect(bx, by, bw, bh, OCOL, "#1e1e1e"))
E.append(
    center_in_box(
        bx, by, bw, bh, "📤  Export  (Excalidraw · Mermaid · JSON)", size=13, bold=True
    )
)

# Downward arrow from engine to output
E.extend(
    arrow(MX + MWID // 2, L2_Y + L2_H, 420, L4_Y + 15, "#e8590c", "dashed", "output")
)

# ═══════════════════════════════════════════════════════════════════════════
# 5. DOWNWARD ARROW: CLI → Engine
# ═══════════════════════════════════════════════════════════════════════════
E.extend(arrow(610, L1_Y + L1_H, 610, L2_Y, "#1971c2", "solid", "dispatch"))

# ═══════════════════════════════════════════════════════════════════════════
# 6. LEGEND
# ═══════════════════════════════════════════════════════════════════════════
leg_y = 780
E.append(rect(40, leg_y, 1190, 36, "#f8f9fa", "#adb5bd"))
E.append(
    txt(
        50,
        leg_y + 8,
        1170,
        24,
        "Legend:  🟦 CLI  🟩 Collector  🟨 Data Model  🟪 Renderer  🟥 Source  🟨 Output  — ▶ data flow  — ╌ internal",
        size=11,
        color="#495057",
        align="left",
    )
)

footer_y = 835
E.append(
    txt(
        380,
        footer_y,
        520,
        16,
        "Generated by excalidraw-diagram-generator  ·  Arch-Viz Design Doc",
        size=10,
        color="#adb5bd",
    )
)

# ─── Validation ──────────────────────────────────────────────────────────

# Check for duplicate IDs
ids = [el["id"] for el in E]
dup_ids = [i for i in ids if ids.count(i) > 1]
if dup_ids:
    raise RuntimeError(f"DUPLICATE IDs found: {set(dup_ids)}")

# Check roundness
for el in E:
    t = el["type"]
    r = el.get("roundness")
    if t == "rectangle":
        assert r is not None and r.get("type") == 3, f"{el['id']} roundness mismatch"
    elif t == "arrow":
        assert r is not None and r.get("type") == 2, f"{el['id']} roundness mismatch"
    elif t == "text":
        assert r is None, f"{el['id']} text roundness should be null"

# Check no forbidden bindings
for el in E:
    assert el.get("boundElements") is None, f"{el['id']} has boundElements"
    assert el.get("containerId") is None, f"{el['id']} has containerId"
    if el["type"] == "text":
        assert el.get("autoResize") is False, f"{el['id']} autoResize should be False"

# Check fontFamily
for el in E:
    if "fontFamily" in el:
        assert el["fontFamily"] in (1, 2, 3), (
            f"{el['id']} fontFamily={el['fontFamily']}"
        )

# ─── Assemble & Write ────────────────────────────────────────────────────

diagram = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": E,
    "appState": {
        "viewBackgroundColor": "#ffffff",
        "gridSize": 20,
    },
    "files": {},
}

output = "arch-viz-architecture.excalidraw"
with open(output, "w", encoding="utf-8") as f:
    json.dump(diagram, f, indent=2, ensure_ascii=False)

print(f"✅  Generated: {output}")
print(f"   Elements:        {len(E)}")
print(f"   Rectangles:      {sum(1 for e in E if e['type'] == 'rectangle')}")
print(f"   Texts:           {sum(1 for e in E if e['type'] == 'text')}")
print(f"   Arrows:          {sum(1 for e in E if e['type'] == 'arrow')}")
print(f"   Validated:       all constraints passed")
print(f"")
print(f"   Open at https://excalidraw.com → drag & drop the file")
