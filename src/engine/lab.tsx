import React from "react";
import {useCurrentFrame} from "remotion";
import {C, cf, Cue, FONT, MONO, prog, bump, W} from "../theme";
import {Stage} from "../scenes";
import {Icon} from "./icons";
const wrap = (t: string, max: number): string[] => {
  const out: string[] = [];
  let cur = "";
  for (const w of t.split(" ")) {
    if ((cur + " " + w).trim().length > max) { out.push(cur); cur = w; } else cur = (cur + " " + w).trim();
  }
  if (cur) out.push(cur);
  return out;
};

type P = {data: any; cues: Cue[]; frames: number; kicker: string; script: any};

const SUFFIX: Record<string, string> = {
  user: ">", exec: "#", cfg: "(config)#", if: "(config-if)#", range: "(config-if-range)#", vlan: "(config-vlan)#",
  router: "(config-router)#", sub: "(config-subif)#", line: "(config-line)#", acl: "(config-ext-nacl)#", dhcp: "(dhcp-config)#",
};
const ICON: Record<string, string> = {switch: "switch", router: "router", pc: "laptop", server: "server", cloud: "cloud", l3: "switch", fw: "shield"};
const LEVEL_COLOR: Record<string, string> = {BASIC: C.lime, INTERMEDIATE: C.cyan, ADVANCED: C.orange};

/* ------------------------------------------------------------ topology */
const Topology: React.FC<{topo: any; x: number; y: number; w: number; h: number; active?: string; f: number; scale?: number; reveal?: number}> = ({topo, x, y, w, h, active, f, scale = 1, reveal = 1}) => {
  const nodes: any[] = topo.nodes;
  const pos = (id: string) => {
    const n = nodes.find((q) => q.id === id)!;
    return {x: x + (n.x / 100) * w, y: y + (n.y / 100) * h};
  };
  return (
    <g>
      <rect x={x - 24} y={y - 34} width={w + 48} height={h + 96} rx={22} fill={C.panel} fillOpacity={0.55} stroke={C.line} strokeWidth={2} />
      {topo.links.map((l: any, i: number) => {
        const a = pos(l.a), b = pos(l.b);
        const dash = l.kind === "trunk" ? "0" : l.kind === "wan" ? "10 8" : "0";
        const col = l.kind === "trunk" ? C.violet : C.muted;
        return (
          <g key={i} opacity={reveal}>
            <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={col} strokeWidth={l.kind === "trunk" ? 7 : 4} strokeDasharray={dash} strokeLinecap="round" />
            {l.la && <text x={a.x + (b.x - a.x) * 0.26} y={a.y + (b.y - a.y) * 0.26 - 8} fontSize={19 * scale} fill={C.muted} fontFamily={MONO} textAnchor="middle">{l.la}</text>}
            {l.lb && <text x={a.x + (b.x - a.x) * 0.74} y={a.y + (b.y - a.y) * 0.74 - 8} fontSize={19 * scale} fill={C.muted} fontFamily={MONO} textAnchor="middle">{l.lb}</text>}
            {l.label && <text x={(a.x + b.x) / 2} y={(a.y + b.y) / 2 + 28} fontSize={20 * scale} fill={col} fontFamily={FONT} fontWeight={700} textAnchor="middle">{l.label}</text>}
          </g>
        );
      })}
      {nodes.map((n, i) => {
        const p = pos(n.id);
        const on = active === n.id;
        const r = 36 * scale;
        const col = n.color ?? (on ? C.cyan : C.text);
        return (
          <g key={n.id} opacity={reveal}>
            {on && <circle cx={p.x} cy={p.y} r={r + 12 + bump(f % 60, 0, 60, 18) * 8} fill={C.cyan} fillOpacity={0.14} stroke={C.cyan} strokeWidth={3} />}
            <circle cx={p.x} cy={p.y} r={r} fill={C.bg} stroke={col} strokeWidth={on ? 5 : 3} />
            <Icon name={ICON[n.type] ?? "box"} x={p.x} y={p.y} s={0.78 * scale} color={col} />
            {n.pos === "top" ? (
              <>
                <text x={p.x} y={p.y - r - 26 * scale - (n.sub ? 24 * scale : 0)} fontSize={24 * scale} fontFamily={FONT} fontWeight={800} fill={on ? C.cyan : C.text} textAnchor="middle">{n.label ?? n.id}</text>
                {n.sub && <text x={p.x} y={p.y - r - 26 * scale} fontSize={19 * scale} fontFamily={MONO} fill={C.muted} textAnchor="middle">{n.sub}</text>}
              </>
            ) : (
              <>
                <text x={p.x} y={p.y + r + 28 * scale} fontSize={24 * scale} fontFamily={FONT} fontWeight={800} fill={on ? C.cyan : C.text} textAnchor="middle">{n.label ?? n.id}</text>
                {n.sub && <text x={p.x} y={p.y + r + 52 * scale} fontSize={19 * scale} fontFamily={MONO} fill={C.muted} textAnchor="middle">{n.sub}</text>}
              </>
            )}
          </g>
        );
      })}
    </g>
  );
};

/* -------------------------------------------------------------- intro */
export const LabIntroS: React.FC<P> = ({data, cues, kicker, script}) => {
  const f = useCurrentFrame();
  const items: {t: string; cue: number}[] = data.items;
  const lvl = script.level as string;
  const lc = LEVEL_COLOR[lvl] ?? C.cyan;
  return (
    <Stage cues={cues} kicker={kicker}>
      <g opacity={prog(f, 2, 16)}>
        <rect x={110} y={120} width={330} height={52} rx={26} fill={lc} fillOpacity={0.16} stroke={lc} strokeWidth={3} />
        <text x={275} y={156} fontSize={26} fontWeight={800} fontFamily={FONT} fill={lc} textAnchor="middle" letterSpacing={2}>{`PART ${script.part} OF ${script.parts} · ${lvl}`}</text>
        <text x={110} y={262} fontSize={70} fontWeight={800} fontFamily={FONT} fill={C.text} letterSpacing={-1}>{script.labTitle}</text>
        <text x={110} y={318} fontSize={34} fontWeight={500} fontFamily={FONT} fill={C.muted}>{script.labSub}</text>
      </g>
      <text x={110} y={420} fontSize={30} fontWeight={800} fontFamily={FONT} fill={C.cyan} letterSpacing={2} opacity={prog(f, 10, 16)}>IN THIS PART YOU WILL</text>
      {items.map((it, i) => {
        const a = prog(f, cf(cues, it.cue), 16);
        const y = 480 + i * 92;
        return (
          <g key={i} opacity={a} transform={`translate(${(1 - a) * -30} 0)`}>
            <circle cx={134} cy={y - 10} r={20} fill={lc} />
            <text x={134} y={y - 1} fontSize={26} fontWeight={800} fontFamily={FONT} fill={C.bg} textAnchor="middle">{i + 1}</text>
            {wrap(it.t, 34).map((ln, k) => (
              <text key={k} x={176} y={y + k * 34} fontSize={32} fontWeight={600} fontFamily={FONT} fill={C.text}>{ln}</text>
            ))}
          </g>
        );
      })}
      <Topology topo={script.topology} x={1120} y={250} w={620} h={440} f={f} reveal={prog(f, 20, 24)} />
    </Stage>
  );
};

/* ---------------------------------------------------------------- cli */
type Ln = {kind: "cmd" | "out"; prompt?: string; text: string; t0: number; dur: number; hl?: boolean; err?: boolean; epoch: number; step: number};

const build = (data: any, cues: Cue[], frames: number): Ln[] => {
  const steps: any[] = data.steps;
  const out: Ln[] = [];
  let epoch = 0;
  let prevDev: string = data.device;
  steps.forEach((st, i) => {
    const sd = st.dev ?? data.device;
    if (st.clear || (i > 0 && sd !== prevDev)) epoch++;
    prevDev = sd;
    const s = cf(cues, st.cue) + 4;
    const e = i + 1 < steps.length ? cf(cues, steps[i + 1].cue) : frames - 24;
    const win = Math.max(20, e - s - 10);
    const dev = st.dev ?? data.device;
    const items: any[] = [];
    for (const raw of st.lines) {
      const ln = typeof raw === "string" ? {c: raw} : raw;
      const mode = ln.p ?? st.p ?? "cfg";
      const d = ln.d ?? dev;
      if (ln.c) items.push({kind: "cmd", prompt: d + (SUFFIX[mode] ?? mode), text: ln.c, nat: Math.max(10, ln.c.length * 1.05) + 8});
      for (const o of ln.out ?? []) {
        const hl = (st.hl ?? []).some((h: string) => o.includes(h));
        items.push({kind: "out", text: o, hl, err: o.startsWith("%"), nat: 1.8});
      }
      if ((ln.out ?? []).length && items.length) items[items.length - 1].nat += 8;
    }
    const natural = items.reduce((a, q) => a + q.nat, 0);
    const k = Math.min(1, (win * 0.86) / natural);
    let t = s;
    for (const q of items) {
      const dur = q.nat * k;
      out.push({kind: q.kind, prompt: q.prompt, text: q.text, t0: t, dur: q.kind === "cmd" ? Math.max(6, dur - 8 * k) : 0, hl: q.hl, err: q.err, epoch, step: i});
      t += dur;
    }
  });
  return out;
};

export const CliS: React.FC<P> = ({data, cues, frames, kicker, script}) => {
  const f = useCurrentFrame();
  const lines = React.useMemo(() => build(data, cues, frames), [data, cues, frames]);
  const steps: any[] = data.steps;
  // current step
  let cur = 0;
  steps.forEach((st, i) => {
    if (f >= cf(cues, st.cue)) cur = i;
  });
  const st = steps[cur];
  const dev = st.dev ?? data.device;
  const started = lines.filter((l) => f >= l.t0);
  const epoch = started.length ? started[started.length - 1].epoch : 0;
  const N = 17;
  const shown = started.filter((l) => l.epoch === epoch).slice(-N);
  const lh = 37.5;
  const x0 = 700;
  const y0 = 238;
  const last = shown[shown.length - 1];
  const typing = last && last.kind === "cmd" && f < last.t0 + last.dur;
  const lc = LEVEL_COLOR[script.level] ?? C.cyan;
  const noteA = prog(f, cf(cues, st.cue), 14);
  return (
    <Stage cues={cues} kicker={kicker}>
      {/* left: topology + plain-english note */}
      <Topology topo={data.topology ?? script.topology} x={96} y={178} w={470} h={300} f={f} active={dev === "ALL" ? undefined : st.node ?? dev} scale={0.82} />
      {(() => {
        const nl = wrap(st.note ?? "", 28);
        const nh = 78 + nl.length * 42;
        const firstCmd = (st.lines as any[]).map((q) => (typeof q === "string" ? q : q.c))[0];
        const key = st.key ?? firstCmd;
        const kl = key ? wrap(key, 31) : [];
        const ky = 560 + nh + 22;
        return (
          <g opacity={noteA}>
            <rect x={72} y={560} width={560} height={nh} rx={22} fill={C.panel} stroke={lc} strokeWidth={3} />
            <text x={104} y={606} fontSize={22} fontWeight={800} fontFamily={FONT} fill={lc} letterSpacing={2}>IN PLAIN ENGLISH</text>
            {nl.map((ln, i) => (
              <text key={i} x={104} y={656 + i * 42} fontSize={32} fontWeight={600} fontFamily={FONT} fill={C.text}>{ln}</text>
            ))}
            {key && ky + 70 + kl.length * 34 < 900 && (
              <g>
                <rect x={72} y={ky} width={560} height={64 + kl.length * 34} rx={22} fill="#060C1A" stroke={C.line} strokeWidth={3} />
                <text x={104} y={ky + 38} fontSize={20} fontWeight={800} fontFamily={FONT} fill={C.muted} letterSpacing={2}>KEY COMMAND</text>
                {kl.map((ln, i) => (
                  <text key={i} x={104} y={ky + 74 + i * 34} fontSize={26} fontWeight={700} fontFamily={MONO} fill={C.cyan}>{ln}</text>
                ))}
              </g>
            )}
          </g>
        );
      })()}
      {/* right: terminal */}
      <rect x={668} y={140} width={1190} height={750} rx={22} fill="#060C1A" stroke={C.line} strokeWidth={3} />
      <rect x={668} y={140} width={1190} height={62} rx={22} fill={C.panel2} />
      <rect x={668} y={180} width={1190} height={22} fill={C.panel2} />
      {[0, 1, 2].map((k) => <circle key={k} cx={706 + k * 26} cy={171} r={8} fill={[C.red, C.orange, C.lime][k]} opacity={0.85} />)}
      <text x={1263} y={180} fontSize={24} fontFamily={MONO} fontWeight={700} fill={C.muted} textAnchor="middle">{`${dev} — console`}</text>
      {shown.map((l, i) => {
        const y = y0 + i * lh;
        if (l.kind === "out") {
          return (
            <g key={l.t0 + "-" + i}>
              {l.hl && <rect x={688} y={y - 28} width={1150} height={lh - 2} rx={8} fill={C.lime} fillOpacity={0.16} stroke={C.lime} strokeOpacity={0.55} strokeWidth={2} />}
              <text x={x0} y={y} fontSize={26} fontFamily={MONO} fill={l.err ? C.orange : l.hl ? C.lime : "#AEBFDD"} fontWeight={l.hl ? 700 : 400} xmlSpace="preserve" style={{whiteSpace: "pre"}}>{l.text}</text>
            </g>
          );
        }
        const n = Math.min(l.text.length, Math.floor(((f - l.t0) / Math.max(1, l.dur)) * l.text.length) + 1);
        const txt = l.text.slice(0, f >= l.t0 + l.dur ? l.text.length : n);
        const isLast = i === shown.length - 1;
        return (
          <g key={l.t0 + "-" + i}>
            <text x={x0} y={y} fontSize={26} fontFamily={MONO} fontWeight={700} xmlSpace="preserve" style={{whiteSpace: "pre"}}>
              <tspan fill={C.sky}>{l.prompt} </tspan>
              <tspan fill={C.text}>{txt}</tspan>
            </text>
            {isLast && (typing || Math.floor(f / 15) % 2 === 0) && (
              <rect x={x0 + (l.prompt!.length + 1 + txt.length) * 15.65} y={y - 24} width={14} height={30} fill={C.cyan} opacity={0.85} />
            )}
          </g>
        );
      })}
    </Stage>
  );
};

void W;
