import React from "react";
import {interpolate, useCurrentFrame} from "remotion";
import {C, cf, Check, Cue, FONT, MONO, prog, W} from "../theme";
import {Stage} from "../scenes";
import {Icon} from "./icons";
import {LabIntroS, CliS} from "./lab";

export type SceneData = {
  id: string;
  type: "hook" | "story" | "flow" | "versus" | "terminal" | "traps" | "recap" | "labintro" | "cli";
  narration: string;
  heading?: string;
  [k: string]: any;
};
type P = {data: SceneData; cues: Cue[]; frames: number; kicker: string; script?: any};

const PAL = [C.cyan, C.lime, C.orange, C.violet, C.sky];
const col = (i: number) => PAL[i % PAL.length];

export const wrap = (t: string, max: number): string[] => {
  const words = t.split(" ");
  const out: string[] = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > max) {
      out.push(cur);
      cur = w;
    } else cur = (cur + " " + w).trim();
  }
  if (cur) out.push(cur);
  return out;
};

const T: React.FC<{x: number; y: number; t: string; size?: number; color?: string; weight?: number; anchor?: "start" | "middle" | "end"; opacity?: number; mono?: boolean; max?: number; lh?: number}> = ({
  x,
  y,
  t,
  size = 32,
  color = C.text,
  weight = 700,
  anchor = "start",
  opacity = 1,
  mono,
  max,
  lh = 1.22,
}) => {
  const lines = max ? wrap(t, max) : [t];
  return (
    <text x={x} y={y} textAnchor={anchor} fontFamily={mono ? MONO : FONT} fontSize={size} fontWeight={weight} fill={color} opacity={opacity}>
      {lines.map((l, i) => (
        <tspan key={i} x={x} dy={i === 0 ? 0 : size * lh}>
          {l}
        </tspan>
      ))}
    </text>
  );
};

const Heading: React.FC<{text?: string; opacity?: number}> = ({text, opacity = 1}) =>
  text ? <T x={W / 2} y={178} t={text} size={54} anchor="middle" weight={800} opacity={opacity} /> : null;

/** appearance + "currently active" helpers for cue-driven items */
const useItem = (cues: Cue[], items: {cue: number}[], i: number, f: number) => {
  const start = cf(cues, items[i].cue);
  const next = i + 1 < items.length ? cf(cues, items[i + 1].cue) : Infinity;
  return {a: prog(f, start, 16), active: f >= start && f < next};
};

/* ------------------------------------------------------------------ hook */
export const HookS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const lines: {t: string; cue: number; color?: string}[] = data.lines ?? [];
  const bob = Math.sin(f / 18) * 6;
  return (
    <Stage cues={cues} kicker={kicker}>
      {data.icon && <Icon name={data.icon} x={W / 2} y={250 + bob} s={3.2} color={C.cyan} opacity={prog(f, 4, 24)} w={5} />}
      {lines.map((l, i) => {
        const a = prog(f, cf(cues, l.cue), 20);
        return (
          <g key={i} transform={`translate(0 ${(1 - a) * 24})`}>
            <T x={W / 2} y={470 + i * 118} t={l.t} size={i === 0 ? 66 : 58} anchor="middle" weight={800} color={l.color ?? (i === 0 ? C.text : col(i))} opacity={a} max={44} />
          </g>
        );
      })}
    </Stage>
  );
};

/* ----------------------------------------------------------------- story */
export const StoryS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const items: {icon: string; story: string; real: string; sub?: string; cue: number}[] = data.items;
  const n = items.length;
  const rh = Math.min(128, 640 / n);
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading} opacity={prog(f, 4, 16)} />
      <T x={300} y={236} t="IN THE STORY" size={22} color={C.muted} weight={700} opacity={prog(f, 8, 14)} />
      <T x={1090} y={236} t="IN THE NETWORK" size={22} color={C.muted} weight={700} opacity={prog(f, 8, 14)} />
      {items.map((it, i) => {
        const {a, active} = useItem(cues, items, i, f);
        const y = 262 + i * rh;
        const c = col(i);
        return (
          <g key={i} opacity={a} transform={`translate(${(1 - a) * -40} 0)`}>
            <rect x={160} y={y} width={1600} height={rh - 16} rx={22} fill={C.panel} stroke={active ? c : C.line} strokeWidth={active ? 4 : 2} />
            <circle cx={236} cy={y + (rh - 16) / 2} r={34} fill={C.bg} stroke={c} strokeWidth={3} />
            <Icon name={it.icon} x={236} y={y + (rh - 16) / 2} s={0.9} color={c} />
            <T x={300} y={y + (rh - 16) / 2 + 12} t={it.story} size={34} weight={600} max={30} />
            <path d={`M 840 ${y + (rh - 16) / 2} H 1000 M 986 ${y + (rh - 16) / 2 - 12} L 1002 ${y + (rh - 16) / 2} L 986 ${y + (rh - 16) / 2 + 12}`} stroke={c} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
            <T x={1090} y={y + (rh - 16) / 2 + (it.sub ? 0 : 12)} t={it.real} size={38} weight={800} color={c} max={28} />
            {it.sub && <T x={1090} y={y + (rh - 16) / 2 + 34} t={it.sub} size={24} weight={500} color={C.muted} max={46} />}
          </g>
        );
      })}
    </Stage>
  );
};

/* ------------------------------------------------------------------ flow */
export const FlowS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const steps: {icon?: string; title: string; sub?: string; cue: number}[] = data.steps;
  const n = steps.length;
  const gap = 56;
  const w = (1680 - (n - 1) * gap) / n;
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading} opacity={prog(f, 4, 16)} />
      {steps.map((s, i) => {
        const {a, active} = useItem(cues, steps, i, f);
        const x = 120 + i * (w + gap);
        const c = col(i);
        return (
          <g key={i} opacity={a} transform={`translate(0 ${(1 - a) * 30})`}>
            {i > 0 && <path d={`M ${x - gap + 10} 510 H ${x - 10} M ${x - 24} 498 L ${x - 10} 510 L ${x - 24} 522`} stroke={C.muted} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />}
            <rect x={x} y={250} width={w} height={520} rx={26} fill={C.panel} stroke={active ? c : C.line} strokeWidth={active ? 5 : 2} />
            <circle cx={x + 44} cy={304} r={28} fill={c} />
            <T x={x + 44} y={315} t={String(i + 1)} size={32} color={C.bg} weight={800} anchor="middle" />
            {s.icon && <Icon name={s.icon} x={x + w / 2} y={430} s={1.9} color={c} />}
            <T x={x + w / 2} y={560} t={s.title} size={n > 4 ? 32 : 40} weight={800} anchor="middle" color={c} max={Math.floor(w / (n > 4 ? 16 : 19))} />
            {s.sub && <T x={x + w / 2} y={n > 4 ? 640 : 650} t={s.sub} size={28} weight={500} anchor="middle" color={C.muted} max={Math.floor(w / 15.5)} />}
          </g>
        );
      })}
    </Stage>
  );
};

/* ---------------------------------------------------------------- versus */
export const VersusS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const rows: {label: string; l: string; r: string; cue: number}[] = data.rows;
  const lc = data.left?.color ?? C.cyan;
  const rc = data.right?.color ?? C.orange;
  const n = rows.length;
  const rh = Math.min(150, 600 / n);
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading} opacity={prog(f, 4, 16)} />
      <g opacity={prog(f, 6, 18)}>
        <rect x={560} y={236} width={560} height={72} rx={20} fill={lc} fillOpacity={0.15} stroke={lc} strokeWidth={3} />
        <T x={840} y={284} t={data.left?.title ?? "A"} size={36} anchor="middle" color={lc} weight={800} />
        <rect x={1160} y={236} width={600} height={72} rx={20} fill={rc} fillOpacity={0.15} stroke={rc} strokeWidth={3} />
        <T x={1460} y={284} t={data.right?.title ?? "B"} size={36} anchor="middle" color={rc} weight={800} />
      </g>
      {rows.map((r, i) => {
        const {a, active} = useItem(cues, rows, i, f);
        const y = 326 + i * rh;
        return (
          <g key={i} opacity={a} transform={`translate(0 ${(1 - a) * 20})`}>
            <rect x={160} y={y} width={1600} height={rh - 14} rx={18} fill={C.panel} stroke={active ? C.text : C.line} strokeWidth={active ? 3 : 2} />
            <T x={190} y={y + (rh - 14) / 2 + 11 - (wrap(r.label, 16).length - 1) * 17} t={r.label} size={30} weight={700} color={C.muted} max={16} />
            <T x={840} y={y + (rh - 14) / 2 + 12 - (wrap(r.l, 24).length - 1) * 18} t={r.l} size={36} anchor="middle" weight={600} color={C.text} max={24} />
            <T x={1460} y={y + (rh - 14) / 2 + 12 - (wrap(r.r, 26).length - 1) * 18} t={r.r} size={36} anchor="middle" weight={600} color={C.text} max={26} />
          </g>
        );
      })}
    </Stage>
  );
};

/* -------------------------------------------------------------- terminal */
export const TerminalS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const lines: {t: string; note?: string; cue: number; color?: string}[] = data.lines;
  const n = lines.length;
  const rh = Math.min(124, 600 / n);
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading} opacity={prog(f, 4, 16)} />
      <rect x={160} y={236} width={1600} height={n * rh + 56} rx={24} fill="#060C1A" stroke={C.line} strokeWidth={3} />
      {[0, 1, 2].map((k) => (
        <circle key={k} cx={200 + k * 26} cy={262} r={8} fill={[C.red, C.orange, C.lime][k]} opacity={0.8} />
      ))}
      {lines.map((l, i) => {
        const {a, active} = useItem(cues, lines, i, f);
        const y = 322 + i * rh;
        return (
          <g key={i} opacity={a}>
            {active && <rect x={180} y={y - 46} width={1560} height={rh - 2} rx={12} fill={l.color ?? C.lime} fillOpacity={0.12} stroke={l.color ?? C.lime} strokeWidth={2.5} />}
            <T x={210} y={y + (l.note ? 0 : 10)} t={l.t} size={36} mono weight={700} color={l.color ?? C.text} />
            {l.note && <T x={210} y={y + 44} t={l.note} size={28} color={C.muted} weight={500} />}
          </g>
        );
      })}
    </Stage>
  );
};

/* ----------------------------------------------------------------- traps */
export const TrapsS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const items: {wrong: string; right: string; cue: number}[] = data.items;
  const n = items.length;
  const rh = Math.min(210, 660 / n);
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading ?? "Common mix-ups"} opacity={prog(f, 4, 16)} />
      {items.map((it, i) => {
        const {a} = useItem(cues, items, i, f);
        const y = 244 + i * rh;
        const h = rh - 18;
        return (
          <g key={i} opacity={a} transform={`translate(0 ${(1 - a) * 24})`}>
            <rect x={140} y={y} width={800} height={h} rx={20} fill={C.red} fillOpacity={0.08} stroke={C.red} strokeWidth={2.5} />
            <Check x={196} y={y + h / 2} ok={false} size={20} />
            <T x={250} y={y + h / 2 - (wrap(it.wrong, 30).length - 1) * 17 + 12} t={it.wrong} size={34} weight={600} color={C.text} max={30} lh={1.2} />
            <rect x={980} y={y} width={800} height={h} rx={20} fill={C.lime} fillOpacity={0.08} stroke={C.lime} strokeWidth={2.5} />
            <Check x={1036} y={y + h / 2} ok size={20} />
            <T x={1090} y={y + h / 2 - (wrap(it.right, 30).length - 1) * 17 + 12} t={it.right} size={34} weight={600} color={C.text} max={30} lh={1.2} />
          </g>
        );
      })}
    </Stage>
  );
};

/* ----------------------------------------------------------------- recap */
export const RecapS: React.FC<P> = ({data, cues, kicker}) => {
  const f = useCurrentFrame();
  const pts: {t: string; cue: number}[] = data.points;
  const cta = prog(f, cf(cues, data.ctaCue ?? cues.length - 1), 18);
  return (
    <Stage cues={cues} kicker={kicker}>
      <Heading text={data.heading ?? "Remember this"} opacity={prog(f, 4, 16)} />
      {pts.map((p, i) => {
        const {a, active} = useItem(cues, pts, i, f);
        const y = 262 + i * 134;
        const c = col(i);
        return (
          <g key={i} opacity={a} transform={`translate(${(1 - a) * -40} 0)`}>
            <rect x={260} y={y} width={1400} height={114} rx={24} fill={C.panel} stroke={active ? c : C.line} strokeWidth={active ? 4 : 2} />
            <circle cx={330} cy={y + 57} r={30} fill={c} />
            <T x={330} y={y + 68} t={String(i + 1)} size={34} anchor="middle" color={C.bg} weight={800} />
            <T x={392} y={y + 57 + 12 - (wrap(p.t, 52).length - 1) * 17} t={p.t} size={36} weight={600} max={52} />
          </g>
        );
      })}
      <g opacity={cta}>
        <rect x={W / 2 - 440} y={836} width={880} height={88} rx={44} fill={C.cyan} />
        <T x={W / 2} y={894} t={data.cta ?? "Try the Courseiva lab"} size={40} anchor="middle" color={C.bg} weight={800} />
      </g>
    </Stage>
  );
};

export const SCENE_TYPES: Record<string, React.FC<P>> = {
  hook: HookS,
  story: StoryS,
  flow: FlowS,
  versus: VersusS,
  terminal: TerminalS,
  traps: TrapsS,
  recap: RecapS,
  labintro: LabIntroS as any,
  cli: CliS as any,
};
void interpolate;
