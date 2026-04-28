import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const GZBRBranding: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Animación de entrada (fade + scale)
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, 30], [0.8, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        opacity,
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          textAlign: 'center',
          padding: '40px',
        }}
      >
        <h1
          style={{
            fontSize: 120,
            fontFamily: 'DM Serif Display, serif',
            color: '#000',
            margin: 0,
            textShadow: '0 0 30px rgba(0,212,255,0.5)',
          }}
        >
          GZBR
        </h1>
        <div
          style={{
            fontSize: 36,
            color: '#000',
            marginTop: 20,
            fontFamily: 'Inter, sans-serif',
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};
