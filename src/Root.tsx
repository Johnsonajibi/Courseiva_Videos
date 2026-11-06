import React from "react";
import {Composition} from "remotion";
import {TopicVideo} from "./engine/Topic";
import {FPS, H, W} from "./theme";

export const Root: React.FC = () => (
  <Composition
    id="Topic"
    component={TopicVideo}
    durationInFrames={30}
    fps={FPS}
    width={W}
    height={H}
    defaultProps={{script: {topic: "x", scenes: []}, timing: {scenes: [], totalFrames: 30}}}
    calculateMetadata={({props}) => ({durationInFrames: Math.max(30, props.timing.totalFrames)})}
  />
);
