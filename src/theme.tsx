import React from "react";
import {Easing, interpolate} from "remotion";

export const W = 1920;
export const H = 1080;
export const FPS = 30;

export const C = {
  bg: "#0A1224",
  bg2: "#0F1B33",
  panel: "#13223F",
  panel2: "#1A2D50",
  line: "#2B4067",
  text: "#EAF0FA",
  muted: "#8FA2C2",
  cyan: "#22D3EE",
  lime: "#A3E635",
  orange: "#FB923C",
  violet: "#A78BFA",
  red: "#F87171",
  sky: "#60A5FA",
};

export const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
export const MONO = "'DejaVu Sans Mono', 'Courier New', monospace";

export const ease = Easing.bezier(0.16, 1, 0.3, 1);

/** 0 -> 1 progress starting at frame `start`, lasting `dur` frames. */
export const prog = (f: number, start: number, dur = 18): number =>
  interpolate(f, [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

/** 0 -> 1 -> 0 bump. */
export const bump = (f: number, start: number, dur = 30, peakAt = 6): number =>
  interpolate(f, [start, start + peakAt, start + dur], [0, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export type Cue = {text: string; start: number; end: number};

/** frame at which cue i starts (scene-local). */
export const cf = (cues: Cue[], i: number): number =>
  Math.round((cues[Math.min(i, cues.length - 1)]?.start ?? 0) * FPS);

/** Collapse spelled-out letters used for speech into display text. */
export const displayText = (s: string): string =>
  s
    .replace(/\b(?:[A-Z] )+[A-Z]s?\b/g, (m) => m.replace(/ /g, ""))
    .replace(/\bO S P F\b/g, "OSPF").replace(/\bA S B R\b/g, "ASBR")
    .replace(/\bA B R\b/g, "ABR")
    .replace(/\bB G P\b/g, "BGP")
    .replace(/\bL S As\b/g, "LSAs")
    .replace(/\bL S A\b/g, "LSA")
    .replace(/\bprocess I D\b/g, "process ID")
    .replace(/\bO, I A\./g, "O IA.")
    .replace(/\bArea zero\b/g, "Area 0")
    .replace(/\bArea one\b/g, "Area 1")
    .replace(/\bType one\b/g, "Type 1")
    .replace(/\bType two\b/g, "Type 2")
    .replace(/\bType three\b/g, "Type 3")
    .replace(/\bType four\b/g, "Type 4")
    .replace(/\bType five\b/g, "Type 5");

export const Router: React.FC<{
  x: number;
  y: number;
  label?: string;
  color?: string;
  r?: number;
  flash?: number;
  ring?: number;
  opacity?: number;
  labelDy?: number;
  fill?: string;
}> = ({x, y, label, color = C.cyan, r = 30, flash = 0, ring = 0, opacity = 1, labelDy, fill}) => {
  const mix = flash > 0 ? C.orange : color;
  return (
    <g opacity={opacity}>
      {ring > 0 && (
        <circle cx={x} cy={y} r={r + 10 + 14 * ring} fill="none" stroke={color} strokeWidth={4} opacity={0.9 * ring} />
      )}
      <circle cx={x} cy={y} r={r} fill={flash > 0 ? C.orange : fill ?? C.panel} fillOpacity={flash > 0 ? 0.25 + 0.55 * flash : 1} stroke={mix} strokeWidth={4} />
      {/* router glyph: crossing arrows */}
      <g stroke={mix} strokeWidth={3} strokeLinecap="round" fill="none">
        <path d={`M ${x - r * 0.5} ${y} H ${x + r * 0.5}`} />
        <path d={`M ${x} ${y - r * 0.5} V ${y + r * 0.5}`} />
        <path d={`M ${x + r * 0.5 - 7} ${y - 6} L ${x + r * 0.5} ${y} L ${x + r * 0.5 - 7} ${y + 6}`} />
        <path d={`M ${x - r * 0.5 + 7} ${y - 6} L ${x - r * 0.5} ${y} L ${x - r * 0.5 + 7} ${y + 6}`} />
        <path d={`M ${x - 6} ${y - r * 0.5 + 7} L ${x} ${y - r * 0.5} L ${x + 6} ${y - r * 0.5 + 7}`} />
        <path d={`M ${x - 6} ${y + r * 0.5 - 7} L ${x} ${y + r * 0.5} L ${x + 6} ${y + r * 0.5 - 7}`} />
      </g>
      {label && (
        <text x={x} y={y + (labelDy ?? r + 30)} textAnchor="middle" fontFamily={FONT} fontSize={24} fontWeight={600} fill={C.text}>
          {label}
        </text>
      )}
    </g>
  );
};

export const Link: React.FC<{
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  color?: string;
  width?: number;
  dash?: string;
  opacity?: number;
  draw?: number;
}> = ({x1, y1, x2, y2, color = C.line, width = 4, dash, opacity = 1, draw = 1}) => {
  const len = Math.hypot(x2 - x1, y2 - y1);
  return (
    <line
      x1={x1}
      y1={y1}
      x2={x2}
      y2={y2}
      stroke={color}
      strokeWidth={width}
      strokeLinecap="round"
      strokeDasharray={dash ?? `${len}`}
      strokeDashoffset={dash ? 0 : len * (1 - draw)}
      opacity={opacity}
    />
  );
};

export const Tag: React.FC<{
  x: number;
  y: number;
  text: string;
  color?: string;
  size?: number;
  opacity?: number;
  solid?: boolean;
  anchor?: "middle" | "start";
}> = ({x, y, text, color = C.cyan, size = 24, opacity = 1, solid = false, anchor = "middle"}) => {
  const w = text.length * size * 0.6 + 36;
  const h = size + 22;
  const x0 = anchor === "middle" ? x - w / 2 : x;
  return (
    <g opacity={opacity}>
      <rect x={x0} y={y - h / 2} width={w} height={h} rx={h / 2} fill={solid ? color : C.bg} fillOpacity={solid ? 1 : 0.85} stroke={color} strokeWidth={3} />
      <text x={x0 + w / 2} y={y + size * 0.35} textAnchor="middle" fontFamily={FONT} fontSize={size} fontWeight={700} fill={solid ? C.bg : color}>
        {text}
      </text>
    </g>
  );
};

export const AreaBox: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  color: string;
  label: string;
  sub?: string;
  opacity?: number;
  scale?: number;
  glow?: number;
}> = ({x, y, w, h, color, label, sub, opacity = 1, scale = 1, glow = 0}) => {
  const cx = x + w / 2;
  const cy = y + h / 2;
  return (
    <g opacity={opacity} transform={`translate(${cx} ${cy}) scale(${scale}) translate(${-cx} ${-cy})`}>
      <rect x={x} y={y} width={w} height={h} rx={34} fill={color} fillOpacity={0.07 + 0.1 * glow} stroke={color} strokeWidth={3 + 3 * glow} strokeDasharray="14 10" />
      <text x={x + 28} y={y + 46} fontFamily={FONT} fontSize={30} fontWeight={800} fill={color}>
        {label}
      </text>
      {sub && (
        <text x={x + 28} y={y + 78} fontFamily={FONT} fontSize={20} fontWeight={500} fill={C.muted}>
          {sub}
        </text>
      )}
    </g>
  );
};

export const Cloud: React.FC<{x: number; y: number; label: string; opacity?: number}> = ({x, y, label, opacity = 1}) => (
  <g opacity={opacity}>
    <path
      d={`M ${x - 90} ${y + 30} a 36 36 0 0 1 8 -70 a 50 50 0 0 1 96 -12 a 40 40 0 0 1 72 40 a 30 30 0 0 1 -8 42 z`}
      fill={C.panel}
      stroke={C.violet}
      strokeWidth={4}
    />
    {label.split("|").map((line, i, all) => (
      <text key={i} x={x} y={y + 2 + (i - (all.length - 1) / 2) * 28} textAnchor="middle" fontFamily={FONT} fontSize={22} fontWeight={700} fill={C.violet}>
        {line}
      </text>
    ))}
  </g>
);

export const Chip: React.FC<{x: number; y: number; text: string; color: string; opacity?: number; scale?: number}> = ({
  x,
  y,
  text,
  color,
  opacity = 1,
  scale = 1,
}) => (
  <g opacity={opacity} transform={`translate(${x} ${y}) scale(${scale})`}>
    <rect x={-34} y={-24} width={68} height={48} rx={12} fill={color} />
    <text x={0} y={9} textAnchor="middle" fontFamily={FONT} fontSize={26} fontWeight={800} fill={C.bg}>
      {text}
    </text>
  </g>
);

export const Check: React.FC<{x: number; y: number; ok: boolean; size?: number; opacity?: number}> = ({x, y, ok, size = 22, opacity = 1}) => (
  <g opacity={opacity} stroke={ok ? C.lime : C.red} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" fill="none">
    {ok ? (
      <path d={`M ${x - size} ${y} L ${x - size * 0.3} ${y + size * 0.7} L ${x + size} ${y - size * 0.7}`} />
    ) : (
      <>
        <path d={`M ${x - size * 0.8} ${y - size * 0.8} L ${x + size * 0.8} ${y + size * 0.8}`} />
        <path d={`M ${x + size * 0.8} ${y - size * 0.8} L ${x - size * 0.8} ${y + size * 0.8}`} />
      </>
    )}
  </g>
);
