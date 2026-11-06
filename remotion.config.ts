import fs from "node:fs";
import {Config} from "@remotion/cli/config";

// Use the system Chrome when present (local box + GitHub runners); otherwise Remotion downloads its own.
const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome";
if (fs.existsSync(chrome)) Config.setBrowserExecutable(chrome);
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(92);
Config.setConcurrency(Number(process.env.CONC || 2));
Config.setCodec("h264");
Config.setCrf(18);
