import React from "react";

/** Simple stroke icons drawn in a -32..32 box. Use <Icon name="key" x y s color /> */
const P: Record<string, React.ReactNode> = {
  person: (
    <>
      <circle cx={0} cy={-12} r={11} />
      <path d="M -22 26 Q -22 4 0 4 Q 22 4 22 26 Z" />
    </>
  ),
  people: (
    <>
      <circle cx={-12} cy={-12} r={9} />
      <circle cx={14} cy={-8} r={8} />
      <path d="M -28 24 Q -28 4 -12 4 Q 2 4 2 24 Z" />
      <path d="M 4 24 Q 4 8 16 8 Q 30 8 30 24" />
    </>
  ),
  building: (
    <>
      <rect x={-20} y={-28} width={40} height={56} rx={3} />
      <path d="M -10 -16 h6 M 4 -16 h6 M -10 -4 h6 M 4 -4 h6 M -10 8 h6 M 4 8 h6" />
      <path d="M -5 28 v-10 h10 v10" />
    </>
  ),
  key: (
    <>
      <circle cx={-14} cy={0} r={11} />
      <path d="M -3 0 H 28 M 18 0 v10 M 26 0 v8" />
    </>
  ),
  envelope: (
    <>
      <rect x={-28} y={-18} width={56} height={36} rx={5} />
      <path d="M -28 -14 L 0 6 L 28 -14" />
    </>
  ),
  book: (
    <>
      <path d="M -28 -20 Q -12 -26 0 -18 Q 12 -26 28 -20 V 20 Q 12 14 0 22 Q -12 14 -28 20 Z" />
      <path d="M 0 -18 V 22" />
    </>
  ),
  door: (
    <>
      <rect x={-16} y={-28} width={32} height={56} rx={3} />
      <circle cx={8} cy={2} r={2.5} />
    </>
  ),
  clock: (
    <>
      <circle cx={0} cy={0} r={26} />
      <path d="M 0 -14 V 0 L 12 8" />
    </>
  ),
  lock: (
    <>
      <rect x={-18} y={-4} width={36} height={28} rx={5} />
      <path d="M -11 -4 V -14 a 11 11 0 0 1 22 0 V -4" />
    </>
  ),
  laptop: (
    <>
      <rect x={-22} y={-20} width={44} height={30} rx={3} />
      <path d="M -30 22 H 30 L 24 10 H -24 Z" />
    </>
  ),
  server: (
    <>
      <rect x={-24} y={-26} width={48} height={20} rx={4} />
      <rect x={-24} y={2} width={48} height={20} rx={4} />
      <circle cx={-14} cy={-16} r={2} />
      <circle cx={-14} cy={12} r={2} />
    </>
  ),
  router: (
    <>
      <circle cx={0} cy={0} r={26} />
      <path d="M -14 0 H 14 M 0 -14 V 14" />
      <path d="M 8 -6 L 14 0 L 8 6 M -8 -6 L -14 0 L -8 6 M -6 8 L 0 14 L 6 8 M -6 -8 L 0 -14 L 6 -8" />
    </>
  ),
  switch: (
    <>
      <rect x={-28} y={-14} width={56} height={28} rx={5} />
      <path d="M -18 -4 h6 M -6 -4 h6 M 6 -4 h6 M -18 6 h6 M -6 6 h6 M 6 6 h6" />
    </>
  ),
  cloud: <path d="M -20 14 a 11 11 0 0 1 2 -22 a 15 15 0 0 1 28 -4 a 12 12 0 0 1 8 26 Z" />,
  mic: (
    <>
      <rect x={-8} y={-26} width={16} height={30} rx={8} />
      <path d="M -18 -2 a 18 18 0 0 0 36 0 M 0 16 V 26 M -10 26 H 10" />
    </>
  ),
  scale: (
    <>
      <path d="M 0 -26 V 24 M -16 24 H 16 M -26 -14 H 26" />
      <path d="M -26 -14 L -34 6 H -18 Z M 26 -14 L 18 6 H 34 Z" />
    </>
  ),
  ruler: (
    <>
      <rect x={-30} y={-10} width={60} height={20} rx={3} />
      <path d="M -20 -10 v8 M -10 -10 v6 M 0 -10 v8 M 10 -10 v6 M 20 -10 v8" />
    </>
  ),
  map: (
    <>
      <path d="M -28 -18 L -10 -24 L 10 -18 L 28 -24 V 18 L 10 24 L -10 18 L -28 24 Z" />
      <path d="M -10 -24 V 18 M 10 -18 V 24" />
    </>
  ),
  bell: (
    <>
      <path d="M -16 14 V -2 a 16 16 0 0 1 32 0 V 14 L 22 20 H -22 Z" />
      <path d="M -5 26 h10" />
    </>
  ),
  shield: <path d="M 0 -28 L 24 -18 V 2 Q 24 20 0 28 Q -24 20 -24 2 V -18 Z" />,
  gear: (
    <>
      <circle cx={0} cy={0} r={9} />
      <circle cx={0} cy={0} r={22} strokeDasharray="8 6" />
    </>
  ),
  list: (
    <>
      <path d="M -24 -16 h6 M -10 -16 h34 M -24 0 h6 M -10 0 h34 M -24 16 h6 M -10 16 h34" />
    </>
  ),
  box: (
    <>
      <path d="M 0 -26 L 24 -14 V 14 L 0 26 L -24 14 V -14 Z" />
      <path d="M -24 -14 L 0 -2 L 24 -14 M 0 -2 V 26" />
    </>
  ),
  wifi: (
    <>
      <path d="M -26 -6 a 36 36 0 0 1 52 0 M -17 4 a 23 23 0 0 1 34 0 M -8 14 a 10 10 0 0 1 16 0" />
      <circle cx={0} cy={22} r={2.5} />
    </>
  ),
  link: (
    <>
      <path d="M -6 6 L 6 -6" />
      <path d="M -10 -2 l -8 8 a 9 9 0 0 0 13 13 l 8 -8 M 10 2 l 8 -8 a 9 9 0 0 0 -13 -13 l -8 8" />
    </>
  ),
  wrench: <path d="M 20 -24 a 12 12 0 0 0 -14 16 L -22 16 a 6 6 0 0 0 8 8 L 10 0 a 12 12 0 0 0 16 -14 L 16 -6 L 8 -10 Z" />,
  question: (
    <>
      <path d="M -12 -14 a 12 12 0 1 1 18 10 Q 0 0 0 8" />
      <circle cx={0} cy={22} r={2.5} />
    </>
  ),
  tree: (
    <>
      <circle cx={0} cy={-18} r={7} />
      <circle cx={-18} cy={14} r={7} />
      <circle cx={18} cy={14} r={7} />
      <path d="M -4 -12 L -15 8 M 4 -12 L 15 8" />
    </>
  ),
  road: (
    <>
      <path d="M -10 -28 L -24 28 M 10 -28 L 24 28" />
      <path d="M 0 -24 V -14 M 0 -4 V 6 M 0 16 V 26" />
    </>
  ),
  stamp: (
    <>
      <path d="M -10 -26 H 10 V -6 H 22 V 8 H -22 V -6 H -10 Z" />
      <path d="M -26 24 H 26" />
    </>
  ),
};

export const ICON_NAMES = Object.keys(P);

export const Icon: React.FC<{name: string; x: number; y: number; s?: number; color: string; opacity?: number; w?: number}> = ({
  name,
  x,
  y,
  s = 1,
  color,
  opacity = 1,
  w = 4,
}) => (
  <g
    opacity={opacity}
    transform={`translate(${x} ${y}) scale(${s})`}
    fill="none"
    stroke={color}
    strokeWidth={w / s}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {P[name] ?? P["box"]}
  </g>
);
