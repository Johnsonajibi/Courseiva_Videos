import React from "react";
import {AbsoluteFill, interpolate, useCurrentFrame} from "remotion";
import {
  AreaBox,
  bump,
  C,
  cf,
  Check,
  Chip,
  Cloud,
  Cue,
  displayText,
  FONT,
  FPS,
  H,
  Link,
  lerp,
  MONO,
  prog,
  Router,
  Tag,
  W,
} from "./theme";

type SceneProps = {cues: Cue[]; frames: number};

/* ------------------------------------------------------------------ frame */
export const Stage: React.FC<{cues: Cue[]; children: React.ReactNode; kicker: string}> = ({cues, children, kicker}) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const cur = cues.find((c) => t >= c.start - 0.05 && t <= c.end + 0.25);
  return (
    <AbsoluteFill style={{background: `radial-gradient(1200px 700px at 50% 38%, ${C.bg2}, ${C.bg})`, fontFamily: FONT}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: "absolute", inset: 0}}>
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#ffffff" strokeOpacity="0.035" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width={W} height={H} fill="url(#grid)" />
        {children}
      </svg>
      <div style={{position: "absolute", left: 64, top: 44, color: C.muted, fontSize: 24, fontWeight: 600, letterSpacing: 1.5}}>
        {kicker}
      </div>
      <div style={{position: "absolute", right: 64, top: 38, color: C.text, fontSize: 32, fontWeight: 800, letterSpacing: -0.5}}>
        course<span style={{color: C.cyan}}>iva</span>
      </div>
      <div style={{position: "absolute", left: 0, right: 0, bottom: 46, display: "flex", justifyContent: "center", minHeight: 96}}>
        {cur && (
          <div
            style={{
              maxWidth: 1560,
              background: "rgba(10,18,36,0.86)",
              border: `1px solid ${C.line}`,
              borderRadius: 18,
              padding: "16px 30px",
              color: C.text,
              fontSize: 36,
              lineHeight: 1.3,
              fontWeight: 500,
              textAlign: "center",
              opacity: interpolate(t, [cur.start - 0.05, cur.start + 0.12], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"}),
            }}
          >
            {displayText(cur.text)}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

const Title: React.FC<{x?: number; y: number; text: string; color?: string; size?: number; opacity?: number}> = ({
  x = W / 2,
  y,
  text,
  color = C.text,
  size = 64,
  opacity = 1,
}) => (
  <text x={x} y={y} textAnchor="middle" fontFamily={FONT} fontSize={size} fontWeight={800} fill={color} opacity={opacity} letterSpacing={-1}>
    {text}
  </text>
);

/* ------------------------------------------------------------- 1. hook */
export const HookScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const xs = [360, 600, 840, 1080, 1320, 1560];
  const ys = [400, 590, 780];
  const nodes: {x: number; y: number}[] = [];
  ys.forEach((y) => xs.forEach((x) => nodes.push({x, y})));
  const idx = (c: number, r: number) => r * xs.length + c;
  const links: [number, number][] = [];
  for (let r = 0; r < ys.length; r++) {
    for (let c = 0; c < xs.length; c++) {
      if (c + 1 < xs.length) links.push([idx(c, r), idx(c + 1, r)]);
      if (r + 1 < ys.length) links.push([idx(c, r), idx(c, r + 1)]);
      if (r + 1 < ys.length && c + 1 < xs.length && (c + r) % 2 === 0) links.push([idx(c, r), idx(c + 1, r + 1)]);
    }
  }
  const flapA = idx(2, 1);
  const flapB = idx(3, 1);
  const flapAt = cf(cues, 1) + 45;
  const rippleAt = flapAt + 14;
  const mid = {x: (nodes[flapA].x + nodes[flapB].x) / 2, y: nodes[flapA].y};
  const flapOn = f >= flapAt;
  const headline1 = interpolate(f, [0, 16, cf(cues, 2) - 14, cf(cues, 2)], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const headline2 = prog(f, cf(cues, 2), 22);
  const dim = interpolate(f, [cf(cues, 2), cf(cues, 2) + 25], [1, 0.3], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <Stage cues={cues} kicker="CCNA 200-301 · OSPF · IP CONNECTIVITY">
      <g opacity={dim}>
        {links.map(([a, b], i) => {
          const broken = (a === flapA && b === flapB) || (a === flapB && b === flapA);
          return (
            <Link
              key={i}
              x1={nodes[a].x}
              y1={nodes[a].y}
              x2={nodes[b].x}
              y2={nodes[b].y}
              color={broken && flapOn ? C.red : C.line}
              dash={broken && flapOn ? "12 12" : undefined}
              width={broken && flapOn ? 6 : 4}
              draw={prog(f, 6 + (i % 9) * 2, 20)}
            />
          );
        })}
        {nodes.map((n, i) => {
          const d = Math.hypot(n.x - mid.x, n.y - mid.y);
          const flash = bump(f, rippleAt + d / 14, 30, 7);
          return <Router key={i} x={n.x} y={n.y} r={28} flash={flash} opacity={prog(f, 4 + (i % 6) * 2, 14)} />;
        })}
        {flapOn && <Check x={mid.x} y={mid.y} ok={false} size={22} opacity={prog(f, flapAt, 8)} />}
        {f >= rippleAt && (
          <Tag x={W / 2} y={890} text="Every router reruns SPF" color={C.orange} size={30} opacity={prog(f, rippleAt + 10, 14)} />
        )}
      </g>
      <Title y={190} text="One flat OSPF area" opacity={headline1} />
      <Title y={190} text="Multi-Area OSPF" color={C.cyan} size={84} opacity={headline2} />
      {f >= cf(cues, 2) && (
        <text x={W / 2} y={285} textAnchor="middle" fontFamily={FONT} fontSize={32} fontWeight={500} fill={C.muted} opacity={prog(f, cf(cues, 2) + 14, 20)}>
          Smaller databases. Faster convergence.
        </text>
      )}
    </Stage>
  );
};

/* ------------------------------------------------------------- 2. areas */
const A1: [number, number][] = [[240, 440], [430, 440], [240, 660], [430, 660], [335, 550]];
const A1L: [number, number][] = [[0, 1], [1, 3], [3, 2], [2, 0], [4, 0], [4, 1], [4, 2], [4, 3]];
const A0: [number, number][] = [[800, 525], [1120, 525], [960, 655]];
const A2: [number, number][] = [[1480, 320], [1680, 320], [1580, 450]];
const A3: [number, number][] = [[1480, 740], [1680, 740], [1580, 850]];
const ABR1 = {x: 630, y: 550};
const ABR2 = {x: 1290, y: 390};
const ABR3 = {x: 1290, y: 700};

export const AreasScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c = [0, 1, 2, 3, 4].map((i) => cf(cues, i));
  const reveal = (d: number) => prog(f, c[0] + d, 22);
  const backboneGlow = interpolate(f, [c[1], c[1] + 14, c[2] - 6, c[2]], [0, 1, 1, 0.25], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const detail = interpolate(f, [c[2], c[2] + 14, c[3] - 4, c[3]], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  // summary chip path: ABR1 -> A0[0] -> A0[1] -> ABR2
  const path = [ABR1, {x: A0[0][0], y: A0[0][1]}, {x: A0[1][0], y: A0[1][1]}, ABR2];
  const pt = interpolate(f, [c[3] + 6, c[3] + 80], [0, 3], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const seg = Math.min(2, Math.floor(pt));
  const sx = lerp(path[seg].x, path[seg + 1].x, pt - seg);
  const sy = lerp(path[seg].y, path[seg + 1].y, pt - seg);
  const flapAt = c[4] + 36;
  const flapOn = f >= flapAt;
  const spf = (d: number) => (flapOn ? bump(f, flapAt + d, 34, 7) : 0);
  const area1Active = flapOn;
  return (
    <Stage cues={cues} kicker="WHY MULTI-AREA">
      <AreaBox x={120} y={300} w={440} h={520} color={C.lime} label="Area 1" opacity={reveal(0)} scale={lerp(0.92, 1, reveal(0))} glow={detail} />
      <AreaBox x={700} y={380} w={520} h={330} color={C.cyan} label="Area 0" sub="Backbone" opacity={reveal(8)} scale={lerp(0.92, 1, reveal(8))} glow={backboneGlow} />
      <AreaBox x={1360} y={200} w={440} h={330} color={C.orange} label="Area 2" opacity={reveal(16)} scale={lerp(0.92, 1, reveal(16))} />
      <AreaBox x={1360} y={620} w={440} h={300} color={C.violet} label="Area 3" opacity={reveal(24)} scale={lerp(0.92, 1, reveal(24))} />

      {/* intra-area links */}
      {A1L.map(([a, b], i) => (
        <Link key={"a1" + i} x1={A1[a][0]} y1={A1[a][1]} x2={A1[b][0]} y2={A1[b][1]} color={detail > 0.2 ? C.lime : C.line} width={4 + 3 * detail} opacity={reveal(6)} />
      ))}
      <Link x1={A0[0][0]} y1={A0[0][1]} x2={A0[1][0]} y2={A0[1][1]} opacity={reveal(12)} color={C.line} />
      <Link x1={A0[1][0]} y1={A0[1][1]} x2={A0[2][0]} y2={A0[2][1]} opacity={reveal(12)} color={C.line} />
      <Link x1={A0[0][0]} y1={A0[0][1]} x2={A0[2][0]} y2={A0[2][1]} opacity={reveal(12)} color={C.line} />
      <Link x1={A2[0][0]} y1={A2[0][1]} x2={A2[1][0]} y2={A2[1][1]} opacity={reveal(20)} />
      <Link x1={A2[0][0]} y1={A2[0][1]} x2={A2[2][0]} y2={A2[2][1]} opacity={reveal(20)} />
      <Link x1={A2[1][0]} y1={A2[1][1]} x2={A2[2][0]} y2={A2[2][1]} opacity={reveal(20)} />
      <Link x1={A3[0][0]} y1={A3[0][1]} x2={A3[1][0]} y2={A3[1][1]} opacity={reveal(28)} />
      <Link x1={A3[0][0]} y1={A3[0][1]} x2={A3[2][0]} y2={A3[2][1]} opacity={reveal(28)} />
      <Link x1={A3[1][0]} y1={A3[1][1]} x2={A3[2][0]} y2={A3[2][1]} opacity={reveal(28)} />
      {/* inter-area links (via ABRs) */}
      {[
        [A1[4], ABR1],
        [ABR1, A0[0]],
        [A0[1], ABR2],
        [ABR2, A2[0]],
        [A0[2], ABR3],
        [ABR3, A3[0]],
      ].map(([p, q], i) => {
        const a = Array.isArray(p) ? {x: p[0], y: p[1]} : (p as {x: number; y: number});
        const b = Array.isArray(q) ? {x: q[0], y: q[1]} : (q as {x: number; y: number});
        return <Link key={"x" + i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} color={backboneGlow > 0.3 ? C.cyan : C.line} width={5} opacity={reveal(30)} />;
      })}
      {/* flap */}
      {flapOn && <Link x1={A1[0][0]} y1={A1[0][1]} x2={A1[2][0]} y2={A1[2][1]} color={C.red} dash="12 12" width={6} />}
      {flapOn && <Check x={240} y={550} ok={false} size={20} opacity={prog(f, flapAt, 8)} />}

      {A1.map((p, i) => (
        <Router key={"r1" + i} x={p[0]} y={p[1]} r={26} color={C.lime} flash={area1Active ? spf(i * 2) : 0} opacity={reveal(8)} />
      ))}
      {A0.map((p, i) => (
        <Router key={"r0" + i} x={p[0]} y={p[1]} r={26} color={C.cyan} opacity={reveal(12)} />
      ))}
      {A2.map((p, i) => (
        <Router key={"r2" + i} x={p[0]} y={p[1]} r={26} color={C.orange} opacity={reveal(20)} />
      ))}
      {A3.map((p, i) => (
        <Router key={"r3" + i} x={p[0]} y={p[1]} r={26} color={C.violet} opacity={reveal(28)} />
      ))}
      {[ABR1, ABR2, ABR3].map((p, i) => (
        <g key={"abr" + i} opacity={reveal(32)}>
          <Router x={p.x} y={p.y} r={30} color={C.text} fill={C.panel2} ring={backboneGlow > 0.5 ? 1 : 0} />
          <text x={p.x} y={p.y - 44} textAnchor="middle" fontFamily={FONT} fontSize={22} fontWeight={800} fill={C.text}>
            ABR
          </text>
        </g>
      ))}

      {/* callouts */}
      {f >= c[1] && f < c[2] + 10 && <Tag x={960} y={335} text="Every area connects to Area 0" color={C.cyan} size={26} opacity={prog(f, c[1] + 4, 14) * (1 - prog(f, c[2] + 8, 8))} />}
      {f >= c[2] && f < c[3] + 5 && <Tag x={340} y={248} text="Full topology detail" color={C.lime} size={26} opacity={prog(f, c[2] + 4, 14) * (1 - prog(f, c[3] + 2, 8))} />}
      {f >= c[3] && f < c[4] && (
        <g opacity={Math.min(1, prog(f, c[3] + 4, 10))}>
          <Tag x={sx} y={sy - 52} text="summary only" color={C.cyan} size={24} solid />
        </g>
      )}
      {flapOn && (
        <>
          <Tag x={340} y={858} text="Area 1 recalculates" color={C.orange} size={26} opacity={prog(f, flapAt + 4, 14)} />
          <Tag x={960} y={770} text="Area 0 unaffected" color={C.lime} size={26} opacity={prog(f, flapAt + 14, 14)} />
          <Tag x={1640} y={246} text="Area 2 unaffected" color={C.lime} size={22} opacity={prog(f, flapAt + 20, 14)} />
          <Tag x={1640} y={666} text="Area 3 unaffected" color={C.lime} size={22} opacity={prog(f, flapAt + 26, 14)} />
        </>
      )}
    </Stage>
  );
};

/* -------------------------------------------------------------- 3. roles */
export const RolesScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c = [0, 1, 2, 3, 4].map((i) => cf(cues, i));
  const base = prog(f, 4, 24);
  const a1: [number, number][] = [[250, 470], [250, 650], [440, 560]];
  const a0: [number, number][] = [[800, 560], [960, 430], [960, 690], [1120, 560]];
  const abrA = {x: 630, y: 560};
  const abrB = {x: 1290, y: 560};
  const asbr = {x: 1560, y: 560};
  const r1 = prog(f, c[1], 16);
  const r2 = prog(f, c[2], 16);
  const r3 = prog(f, c[3], 16);
  const r4 = prog(f, c[4], 16);
  return (
    <Stage cues={cues} kicker="ROUTER ROLES">
      <Title y={190} text="Four router roles" opacity={prog(f, c[0] + 2, 18)} />
      <AreaBox x={110} y={340} w={460} h={440} color={C.lime} label="Area 1" opacity={base} />
      <AreaBox x={700} y={340} w={520} h={440} color={C.cyan} label="Area 0" sub="Backbone" opacity={base} />
      <AreaBox x={1370} y={340} w={440} h={440} color={C.orange} label="Area 2" opacity={base} />

      <g opacity={base}>
        <Link x1={a1[0][0]} y1={a1[0][1]} x2={a1[1][0]} y2={a1[1][1]} />
        <Link x1={a1[0][0]} y1={a1[0][1]} x2={a1[2][0]} y2={a1[2][1]} />
        <Link x1={a1[1][0]} y1={a1[1][1]} x2={a1[2][0]} y2={a1[2][1]} />
        <Link x1={a1[2][0]} y1={a1[2][1]} x2={abrA.x} y2={abrA.y} />
        <Link x1={abrA.x} y1={abrA.y} x2={a0[0][0]} y2={a0[0][1]} />
        <Link x1={a0[0][0]} y1={a0[0][1]} x2={a0[1][0]} y2={a0[1][1]} />
        <Link x1={a0[0][0]} y1={a0[0][1]} x2={a0[2][0]} y2={a0[2][1]} />
        <Link x1={a0[1][0]} y1={a0[1][1]} x2={a0[3][0]} y2={a0[3][1]} />
        <Link x1={a0[2][0]} y1={a0[2][1]} x2={a0[3][0]} y2={a0[3][1]} />
        <Link x1={a0[3][0]} y1={a0[3][1]} x2={abrB.x} y2={abrB.y} />
        <Link x1={abrB.x} y1={abrB.y} x2={asbr.x} y2={asbr.y} />
      </g>
      {a1.map((p, i) => (
        <Router key={"i" + i} x={p[0]} y={p[1]} r={28} color={C.lime} opacity={base} ring={r1} />
      ))}
      {a0.map((p, i) => (
        <Router key={"b" + i} x={p[0]} y={p[1]} r={28} color={C.cyan} opacity={base} ring={r4} />
      ))}
      <Router x={abrA.x} y={abrA.y} r={32} color={C.text} fill={C.panel2} opacity={base} ring={Math.max(r2, r4)} />
      <Router x={abrB.x} y={abrB.y} r={32} color={C.text} fill={C.panel2} opacity={base} ring={Math.max(r2, r4)} />
      <Router x={asbr.x} y={asbr.y} r={32} color={C.orange} fill={C.panel2} opacity={base} ring={r3} />
      {/* external cloud */}
      <g opacity={r3}>
        <Link x1={asbr.x} y1={asbr.y} x2={1640} y2={290} color={C.violet} dash="10 10" />
        <Cloud x={1640} y={225} label="External|BGP / static" />
      </g>
      {/* callouts */}
      <Tag x={340} y={830} text="Internal router" color={C.lime} size={28} opacity={r1} />
      <Tag x={630} y={640} text="ABR" color={C.text} size={28} solid opacity={r2} />
      {/* two databases under the ABR */}
      <g opacity={r2}>
        {[
          {y: 450, t: "Area 1 DB", col: C.lime},
          {y: 398, t: "Area 0 DB", col: C.cyan},
        ].map((d, i) => (
          <g key={i}>
            <rect x={570} y={d.y - 22} width={120} height={44} rx={10} fill={C.panel} stroke={d.col} strokeWidth={3} />
            <text x={630} y={d.y + 7} textAnchor="middle" fontFamily={FONT} fontSize={20} fontWeight={700} fill={d.col}>
              {d.t}
            </text>
          </g>
        ))}
      </g>
      <text x={abrB.x} y={abrB.y + 92} textAnchor="middle" fontFamily={FONT} fontSize={22} fontWeight={800} fill={C.text} opacity={base}>
        ABR
      </text>
      <Tag x={1560} y={650} text="ASBR" color={C.orange} size={28} solid opacity={r3} />
      <Tag x={960} y={830} text="Backbone router: any interface in Area 0" color={C.cyan} size={28} opacity={r4} />
    </Stage>
  );
};

/* --------------------------------------------------------------- 4. LSAs */
const LSA_COL = [C.cyan, C.sky, C.lime, C.orange, C.violet];
const LSA_CARDS = [
  {n: "1", name: "Router LSA", by: "Every router", scope: "Stays in its area"},
  {n: "2", name: "Network LSA", by: "the DR", scope: "Stays in its area"},
  {n: "3", name: "Summary LSA", by: "ABR", scope: "Crosses areas"},
  {n: "4", name: "ASBR summary", by: "ABR", scope: "Where the ASBR is"},
  {n: "5", name: "External LSA", by: "ASBR", scope: "Carries external routes"},
];

export const LsaScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c = [0, 1, 2, 3, 4, 5].map((i) => cf(cues, i));
  const base = prog(f, 4, 24);
  const R = {x: 230, y: 350};
  const DR = {x: 410, y: 350};
  const ABRa = {x: 670, y: 350};
  const M = {x: 960, y: 350};
  const ABRb = {x: 1250, y: 350};
  const ASBR = {x: 1560, y: 350};
  const sway = (start: number) => Math.sin(Math.max(0, f - start) / 5) * 22 * prog(f, start, 10);
  // card reveal: cards 1,2 at c1,c2; card 3 at c4; cards 4,5 at c5
  const cardAt = [c[1], c[2], c[4], c[5], c[5] + 16];
  const t3 = interpolate(f, [c[4] + 6, c[4] + 70], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const t5 = interpolate(f, [c[5] + 40, c[5] + 150], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <Stage cues={cues} kicker="LSA TYPES · OBJECTIVE 3.4">
      <AreaBox x={110} y={190} w={470} h={300} color={C.lime} label="Area 1" opacity={base} />
      <AreaBox x={760} y={190} w={400} h={300} color={C.cyan} label="Area 0" opacity={base} />
      <AreaBox x={1340} y={190} w={470} h={300} color={C.orange} label="Area 2" opacity={base} />
      <g opacity={base}>
        <Link x1={R.x} y1={R.y} x2={DR.x} y2={DR.y} />
        <Link x1={DR.x} y1={DR.y} x2={ABRa.x} y2={ABRa.y} />
        <Link x1={ABRa.x} y1={ABRa.y} x2={M.x} y2={M.y} />
        <Link x1={M.x} y1={M.y} x2={ABRb.x} y2={ABRb.y} />
        <Link x1={ABRb.x} y1={ABRb.y} x2={ASBR.x} y2={ASBR.y} />
      </g>
      <Router x={R.x} y={R.y} r={26} color={C.lime} opacity={base} label="R" labelDy={52} />
      <Router x={DR.x} y={DR.y} r={26} color={C.lime} opacity={base} label="DR" labelDy={52} />
      <Router x={ABRa.x} y={ABRa.y} r={28} color={C.text} fill={C.panel2} opacity={base} label="ABR" labelDy={54} />
      <Router x={M.x} y={M.y} r={26} color={C.cyan} opacity={base} />
      <Router x={ABRb.x} y={ABRb.y} r={28} color={C.text} fill={C.panel2} opacity={base} label="ABR" labelDy={54} />
      <Router x={ASBR.x} y={ASBR.y} r={28} color={C.orange} fill={C.panel2} opacity={base} label="ASBR" labelDy={54} />

      {/* Type 1 / 2 chips bounce inside area 1; barrier at the boundary */}
      {f >= c[1] && <Chip x={R.x + (f >= c[3] ? sway(c[3]) : 0)} y={R.y - 70} text="T1" color={LSA_COL[0]} opacity={prog(f, c[1] + 2, 10)} />}
      {f >= c[2] && <Chip x={DR.x + (f >= c[3] ? sway(c[3] + 4) : 0)} y={DR.y - 70} text="T2" color={LSA_COL[1]} opacity={prog(f, c[2] + 2, 10)} />}
      {f >= c[3] && (
        <g opacity={prog(f, c[3], 12) * (1 - prog(f, c[4], 10))}>
          <rect x={560} y={230} width={14} height={240} rx={7} fill={C.red} />
          <Tag x={570} y={520} text="stays in the area" color={C.red} size={22} />
        </g>
      )}
      {/* Type 3 crosses the ABR */}
      {f >= c[4] && <Chip x={lerp(ABRa.x, M.x, t3)} y={ABRa.y - 72} text="T3" color={LSA_COL[2]} opacity={prog(f, c[4] + 2, 10)} />}
      {/* Type 4 and Type 5 */}
      {f >= c[5] && <Chip x={ASBR.x - 130} y={ASBR.y + 82} text="T4" color={LSA_COL[3]} opacity={prog(f, c[5] + 4, 10)} />}
      {f >= c[5] + 40 && <Chip x={lerp(ASBR.x, DR.x + 40, t5)} y={ASBR.y - 130} text="T5" color={LSA_COL[4]} opacity={prog(f, c[5] + 40, 10)} />}

      {/* cards */}
      {LSA_CARDS.map((card, i) => {
        const x = 105 + i * 355;
        const p = prog(f, cardAt[i], 18);
        return (
          <g key={i} opacity={p} transform={`translate(${x} ${lerp(30, 0, p)})`}>
            <rect x={0} y={590} width={330} height={250} rx={22} fill={C.panel} stroke={LSA_COL[i]} strokeWidth={4} />
            <text x={26} y={668} fontFamily={FONT} fontSize={64} fontWeight={800} fill={LSA_COL[i]}>
              {"Type " + card.n}
            </text>
            <text x={26} y={716} fontFamily={FONT} fontSize={30} fontWeight={700} fill={C.text}>
              {card.name}
            </text>
            <text x={26} y={764} fontFamily={FONT} fontSize={24} fontWeight={500} fill={C.muted}>
              {"Made by: " + card.by}
            </text>
            <text x={26} y={806} fontFamily={FONT} fontSize={24} fontWeight={600} fill={LSA_COL[i]}>
              {card.scope}
            </text>
          </g>
        );
      })}
    </Stage>
  );
};

/* ------------------------------------------------------------ 5. O IA */
export const InterAreaScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c0 = cf(cues, 0);
  const c1 = cf(cues, 1);
  const lines = [
    {t: "R1# show ip route ospf", col: C.muted},
    {t: "O    10.0.1.0/24 [110/2] via 192.168.1.2, Gig0/0", col: C.text},
    {t: "O IA 172.16.0.0/16 [110/20] via 192.168.1.2, Gig0/0", col: C.text},
  ];
  const typed = (i: number) => {
    const start = c0 + 6 + i * 26;
    const n = Math.floor(interpolate(f, [start, start + 24], [0, lines[i].t.length], {extrapolateLeft: "clamp", extrapolateRight: "clamp"}));
    return lines[i].t.slice(0, n);
  };
  const hi = prog(f, c0 + 100, 16);
  const m = (i: number) => prog(f, c1 + i * 14, 16);
  return (
    <Stage cues={cues} kicker="READING THE ROUTING TABLE">
      <g>
        <rect x={130} y={220} width={1130} height={330} rx={22} fill="#070D1A" stroke={C.line} strokeWidth={3} />
        <circle cx={172} cy={258} r={8} fill={C.red} />
        <circle cx={200} cy={258} r={8} fill={C.orange} />
        <circle cx={228} cy={258} r={8} fill={C.lime} />
        <rect x={150} y={430} width={1090} height={64} rx={10} fill={C.lime} fillOpacity={0.16 * hi} stroke={C.lime} strokeOpacity={hi} strokeWidth={3} />
        {lines.map((l, i) => (
          <text key={i} x={162} y={336 + i * 66} fontFamily={MONO} fontSize={30} fill={l.col}>
            {typed(i)}
          </text>
        ))}
        <Tag x={1128} y={400} text="inter-area" color={C.lime} size={22} opacity={hi} />
      </g>
      {/* legend */}
      <g opacity={prog(f, c0 + 90, 18)}>
        <rect x={1320} y={220} width={470} height={330} rx={22} fill={C.panel} stroke={C.line} strokeWidth={3} />
        <text x={1356} y={290} fontFamily={MONO} fontSize={40} fontWeight={700} fill={C.cyan}>O</text>
        <text x={1356} y={334} fontFamily={FONT} fontSize={26} fill={C.text}>Intra-area route</text>
        <text x={1356} y={430} fontFamily={MONO} fontSize={40} fontWeight={700} fill={C.lime}>O IA</text>
        <text x={1356} y={474} fontFamily={FONT} fontSize={26} fill={C.text}>Inter-area route</text>
        <text x={1356} y={512} fontFamily={FONT} fontSize={26} fill={C.muted}>learned from a Type 3 LSA</text>
      </g>
      {/* metric build-up */}
      {[
        {x: 130, w: 470, t1: "Your router → ABR", t2: "your own cost", col: C.sky, i: 0},
        {x: 700, w: 520, t1: "ABR → destination", t2: "cost carried in the Type 3 LSA", col: C.lime, i: 1},
        {x: 1320, w: 470, t1: "Metric in the route", t2: "the sum of both", col: C.orange, i: 2},
      ].map((b) => (
        <g key={b.i} opacity={m(b.i)} transform={`translate(0 ${lerp(24, 0, m(b.i))})`}>
          <rect x={b.x} y={640} width={b.w} height={150} rx={22} fill={C.panel} stroke={b.col} strokeWidth={4} />
          <text x={b.x + 28} y={706} fontFamily={FONT} fontSize={34} fontWeight={800} fill={b.col}>{b.t1}</text>
          <text x={b.x + 28} y={752} fontFamily={FONT} fontSize={26} fill={C.muted}>{b.t2}</text>
        </g>
      ))}
      <text x={650} y={735} textAnchor="middle" fontFamily={FONT} fontSize={60} fontWeight={800} fill={C.text} opacity={m(1)}>+</text>
      <text x={1270} y={735} textAnchor="middle" fontFamily={FONT} fontSize={60} fontWeight={800} fill={C.text} opacity={m(2)}>=</text>
    </Stage>
  );
};

/* ------------------------------------------------------------- 6. stub */
export const StubScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c = [0, 1, 2, 3].map((i) => cf(cues, i));
  const rows = ["Type 1 · Router", "Type 2 · Network", "Type 3 · Summary", "Type 4 · ASBR summary", "Type 5 · External", "Default route"];
  type Cell = "yes" | "no" | string;
  const cols: {name: string; x: number; color: string; at: number; cells: Cell[]}[] = [
    {name: "Standard area", x: 540, color: C.cyan, at: c[0] + 4, cells: ["yes", "yes", "yes", "yes", "yes", "none"]},
    {name: "Stub area", x: 960, color: C.lime, at: c[1] + 4, cells: ["yes", "yes", "yes", "no", "no", "from ABR"]},
    {name: "Totally stubby", x: 1380, color: C.orange, at: c[2] + 4, cells: ["yes", "yes", "default only", "no", "no", "from ABR"]},
  ];
  const y0 = 250;
  const rh = 78;
  const dim = interpolate(f, [c[3], c[3] + 20], [1, 0.5], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <Stage cues={cues} kicker="STUB AND TOTALLY STUBBY AREAS">
      <Title y={170} text="Which LSAs get in?" size={56} opacity={prog(f, 4, 18)} />
      <g opacity={dim}>
        {rows.map((r, i) => (
          <g key={r} opacity={prog(f, c[0] + i * 3, 14)}>
            <rect x={130} y={y0 + i * rh} width={1650} height={rh - 8} rx={12} fill={C.panel} fillOpacity={i % 2 ? 0.5 : 0.8} />
            <text x={156} y={y0 + i * rh + 46} fontFamily={FONT} fontSize={28} fontWeight={600} fill={C.text}>
              {r}
            </text>
          </g>
        ))}
        {cols.map((col) => {
          const p = prog(f, col.at, 16);
          return (
            <g key={col.name} opacity={p}>
              <text x={col.x + 200} y={y0 - 22} textAnchor="middle" fontFamily={FONT} fontSize={32} fontWeight={800} fill={col.color}>
                {col.name}
              </text>
              {col.cells.map((cell, i) => {
                const cy = y0 + i * rh + 31;
                const cx = col.x + 200;
                if (cell === "yes") return <Check key={i} x={cx} y={cy} ok size={18} />;
                if (cell === "no") return <Check key={i} x={cx} y={cy} ok={false} size={16} />;
                return (
                  <text key={i} x={cx} y={cy + 10} textAnchor="middle" fontFamily={FONT} fontSize={26} fontWeight={700} fill={cell === "none" ? C.muted : col.color}>
                    {cell}
                  </text>
                );
              })}
            </g>
          );
        })}
      </g>
      {/* config */}
      {[
        {x: 130, w: 780, h1: "Every router in the area", code: "area 1 stub", col: C.lime},
        {x: 960, w: 820, h1: "ABR only, for totally stubby", code: "area 1 stub no-summary", col: C.orange},
      ].map((b, i) => {
        const p = prog(f, c[3] + i * 16, 16);
        return (
          <g key={i} opacity={p} transform={`translate(0 ${lerp(24, 0, p)})`}>
            <rect x={b.x} y={756} width={b.w} height={170} rx={22} fill="#070D1A" stroke={b.col} strokeWidth={4} />
            <text x={b.x + 30} y={806} fontFamily={FONT} fontSize={26} fontWeight={700} fill={b.col}>{b.h1}</text>
            <text x={b.x + 30} y={878} fontFamily={MONO} fontSize={30} fill={C.text}>{"R(config-router)# " + b.code}</text>
          </g>
        );
      })}
    </Stage>
  );
};

/* ------------------------------------------------------------- 7. traps */
export const TrapsScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c = [0, 1, 2, 3, 4].map((i) => cf(cues, i));
  const cards = [
    {t: "ABR needs the backbone", wrong: "Sits between any two areas", right: "Needs an interface in Area 0", col: C.cyan},
    {t: "Stub flag must match", wrong: "Set it on the ABR only", right: "Every router, or no adjacency", col: C.lime},
    {t: "Area 0 can't be a stub", wrong: "Any area can be a stub", right: "Backbone must carry all routes", col: C.orange},
    {t: "Process ID is local", wrong: "Must match on every router", right: "Only locally significant", col: C.violet},
  ];
  return (
    <Stage cues={cues} kicker="EXAM TRAPS">
      <Title y={170} text="Four traps" size={60} opacity={prog(f, c[0] + 2, 18)} />
      {cards.map((card, i) => {
        const x = 110 + (i % 2) * 860;
        const y = 240 + Math.floor(i / 2) * 330;
        const p = prog(f, c[i + 1], 18);
        return (
          <g key={i} opacity={p} transform={`translate(${x} ${y + lerp(30, 0, p)})`}>
            <rect width={840} height={300} rx={26} fill={C.panel} stroke={card.col} strokeWidth={4} />
            <circle cx={64} cy={64} r={30} fill={card.col} />
            <text x={64} y={76} textAnchor="middle" fontFamily={FONT} fontSize={34} fontWeight={800} fill={C.bg}>{i + 1}</text>
            <text x={118} y={78} fontFamily={FONT} fontSize={38} fontWeight={800} fill={C.text}>{card.t}</text>
            <Check x={60} y={160} ok={false} size={16} />
            <text x={110} y={172} fontFamily={FONT} fontSize={30} fill={C.red}>{card.wrong}</text>
            <Check x={60} y={236} ok size={18} />
            <text x={110} y={248} fontFamily={FONT} fontSize={30} fontWeight={600} fill={C.lime}>{card.right}</text>
          </g>
        );
      })}
    </Stage>
  );
};

/* ------------------------------------------------------------- 8. outro */
export const OutroScene: React.FC<SceneProps> = ({cues}) => {
  const f = useCurrentFrame();
  const c0 = cf(cues, 0);
  const c1 = cf(cues, 1);
  const p0 = prog(f, c0 + 2, 24);
  const items = [
    {k: "LAB", t: "Configure OSPF Multi-Area", col: C.lime},
    {k: "TROUBLESHOOT", t: "OSPF Area Mismatch", col: C.orange},
  ];
  return (
    <Stage cues={cues} kicker="NEXT STEP">
      <text x={W / 2} y={330} textAnchor="middle" fontFamily={FONT} fontSize={150} fontWeight={800} fill={C.text} opacity={p0} letterSpacing={-4}>
        course<tspan fill={C.cyan}>iva</tspan>
      </text>
      {items.map((it, i) => {
        const p = prog(f, c1 + i * 14, 18);
        const x = 220 + i * 760;
        return (
          <g key={i} opacity={p} transform={`translate(${x} ${460 + lerp(26, 0, p)})`}>
            <rect width={720} height={190} rx={26} fill={C.panel} stroke={it.col} strokeWidth={4} />
            <text x={36} y={64} fontFamily={FONT} fontSize={26} fontWeight={800} fill={it.col} letterSpacing={3}>{it.k}</text>
            <text x={36} y={128} fontFamily={FONT} fontSize={44} fontWeight={800} fill={C.text}>{it.t}</text>
          </g>
        );
      })}
      <Tag x={W / 2} y={790} text="courseiva.com" color={C.cyan} size={34} opacity={prog(f, c1 + 30, 16)} />
    </Stage>
  );
};
