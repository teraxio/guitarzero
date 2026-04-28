import React from 'react';
import {Composition} from 'remotion';
import {WonderwallIntro} from './compositions/WonderwallIntro';
import {SevenNationArmy} from './compositions/SevenNationArmy';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="WonderwallIntro"
        component={WonderwallIntro}
        durationInFrames={450} // 15 segundos @ 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
      <Composition
        id="SevenNationArmy"
        component={SevenNationArmy}
        durationInFrames={600} // 20 segundos @ 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};
