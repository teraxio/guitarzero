import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {GZBRBranding} from '../components/GZBRBranding';
import {ChordCircle} from '../components/ChordCircle';
import {TabViewer} from '../components/TabViewer';

export const WonderwallIntro: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Tabs para Wonderwall intro (simplificado)
  const tabs = [
    // Em7
    {string: 1, fret: 0, startFrame: fps * 3, duration: fps * 2},
    {string: 2, fret: 3, startFrame: fps * 3, duration: fps * 2},
    {string: 3, fret: 0, startFrame: fps * 3, duration: fps * 2},
    {string: 4, fret: 2, startFrame: fps * 3, duration: fps * 2},
    {string: 5, fret: 2, startFrame: fps * 3, duration: fps * 2},
    {string: 6, fret: 0, startFrame: fps * 3, duration: fps * 2},
    
    // G
    {string: 1, fret: 3, startFrame: fps * 6, duration: fps * 2},
    {string: 2, fret: 3, startFrame: fps * 6, duration: fps * 2},
    {string: 3, fret: 0, startFrame: fps * 6, duration: fps * 2},
    {string: 4, fret: 0, startFrame: fps * 6, duration: fps * 2},
    {string: 5, fret: 2, startFrame: fps * 6, duration: fps * 2},
    {string: 6, fret: 3, startFrame: fps * 6, duration: fps * 2},
  ];

  return (
    <AbsoluteFill style={{background: '#0a0e12'}}>
      {/* Intro GZBR (3 segundos) */}
      <Sequence from={0} durationInFrames={fps * 3}>
        <GZBRBranding text="Guitar Tutorial" />
      </Sequence>

      {/* Tutorial principal */}
      <Sequence from={fps * 3}>
        <AbsoluteFill>
          {/* Título */}
          <div
            style={{
              position: 'absolute',
              top: 40,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontSize: 48,
              color: '#fff',
              fontFamily: 'DM Serif Display, serif',
            }}
          >
            Wonderwall - Intro
          </div>

          {/* Círculos de acordes */}
          <div
            style={{
              position: 'absolute',
              top: 150,
              left: 0,
              right: 0,
              height: 200,
            }}
          >
            <ChordCircle
              chord="Em7"
              startFrame={fps * 3}
              duration={fps * 3}
              position={0.3}
            />
            <ChordCircle
              chord="G"
              startFrame={fps * 6}
              duration={fps * 3}
              position={0.7}
            />
          </div>

          {/* Tabs */}
          <div style={{position: 'absolute', bottom: 100, left: 0, right: 0}}>
            <TabViewer notes={tabs} />
          </div>

          {/* Progress bar */}
          <div
            style={{
              position: 'absolute',
              bottom: 20,
              left: 50,
              right: 50,
              height: 4,
              background: 'rgba(255,255,255,0.2)',
              borderRadius: 2,
            }}
          >
            <div
              style={{
                width: `${(frame / (fps * 15)) * 100}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #00d4ff, #ff00ff)',
                borderRadius: 2,
              }}
            />
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* Outro */}
      <Sequence from={fps * 12} durationInFrames={fps * 3}>
        <AbsoluteFill
          style={{
            background: 'linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <div style={{textAlign: 'center'}}>
            <h2
              style={{
                fontSize: 60,
                color: '#000',
                fontFamily: 'DM Serif Display, serif',
                margin: 0,
              }}
            >
              ¡Excelente!
            </h2>
            <div style={{fontSize: 32, color: '#000', marginTop: 20}}>
              Siguiente: Seven Nation Army
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
