import {useEffect, useState} from "react";
import {continueRender, delayRender, staticFile} from "remotion";

const FACES: [number, string][] = [
  [400, "Inter-Regular.otf"],
  [500, "Inter-Medium.otf"],
  [600, "Inter-SemiBold.otf"],
  [700, "Inter-Bold.otf"],
  [800, "Inter-ExtraBold.otf"],
];

/** Loads the bundled Inter font so renders look identical on any machine. */
export const useInter = () => {
  const [handle] = useState(() => delayRender("Loading Inter"));
  useEffect(() => {
    Promise.all(FACES.map(([w, f]) => new FontFace("Inter", `url(${staticFile("fonts/" + f)})`, {weight: String(w)}).load()))
      .then((faces) => faces.forEach((f) => document.fonts.add(f)))
      .catch((e) => console.error("font load failed", e))
      .finally(() => continueRender(handle));
  }, [handle]);
};
