import {bundle} from "@remotion/bundler";
import {renderStill, selectComposition} from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";

const topic = process.argv[2];
const timing = JSON.parse(fs.readFileSync(`topics/${topic}/timing.json`, "utf8"));
// busiest moment: near the end of the voice in each scene (override with argv frames)
const frames = process.argv.slice(3).length
  ? process.argv.slice(3).map(Number)
  : timing.scenes.map((s) => s.startFrame + Math.round((s.cues.at(-1).end - 0.3) * timing.fps));
const serveUrl = await bundle({entryPoint: path.resolve("src/index.ts"), webpackOverride: (c) => c});
const propsFile = `topics/${topic}/props.json`;
const inputProps = process.env.COMP === "Topic" ? JSON.parse(fs.readFileSync(propsFile, "utf8")) : undefined;
const comp = await selectComposition({serveUrl, id: process.env.COMP || "OspfMultiAreaLsa", inputProps, browserExecutable: "/usr/bin/google-chrome"});
for (const frame of frames) {
  const output = `stills/${topic}-${String(frame).padStart(5, "0")}.png`;
  await renderStill({composition: comp, serveUrl, inputProps, frame, output, browserExecutable: "/usr/bin/google-chrome", imageFormat: "png"});
  console.log("wrote", output);
}
