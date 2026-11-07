import React from "react";
import {Audio, Sequence, staticFile} from "remotion";
import {SCENE_TYPES} from "./scenes";
import type {Cue} from "../theme";
import {useInter} from "./fonts";

export type TopicProps = {script: any; timing: any};

export const TopicVideo: React.FC<TopicProps> = ({script, timing}) => {
  useInter();
  return (
  <>
    {timing.scenes.map((s: any, i: number) => {
      const data = script.scenes[i];
      const Scene = SCENE_TYPES[data.type];
      if (!Scene) throw new Error(`Unknown scene type ${data.type}`);
      return (
        <Sequence key={s.id} from={s.startFrame} durationInFrames={s.frames}>
          <Audio src={staticFile(`${script.topic}/${s.audio}`)} />
          <Scene data={data} cues={s.cues as Cue[]} frames={s.frames} kicker={script.kicker ?? "BEGINNER'S GUIDE"} script={script} />
        </Sequence>
      );
    })}
  </>
  );
};
