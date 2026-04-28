import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';

interface ChordCircleProps {
  chord: string;
  startFrame: number;
  duration: number;
  position: number; // 0-1 para posición horizontal
}

export const ChordCircle: React.FC<ChordCircleProps> = ({
  chord,
  startFrame,
  duration,
  position,
}) => {
  const frame = useCurrentFrame();

  const isActive = frame >= startFrame && frame < startFrame + duration;

  const scale = interpolate(
    frame,
    [startFrame, startFrame + 10],
    [0.8, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );

  const glow = isActive ? '0 0 40px rgba(0,212,255,1)' : '0 0 10px rgba(0,212,255,0.3)';
  const opacity = isActive ? 1 : 0.5;

  return (
    <div
      style={{
        position: 'absolute',
        left: `${position * 100}%`,
        top: '50%',
        transform: `translate(-50%, -50%) scale(${scale})`,
        width: 150,
        height: 150,
        borderRadius: '50%',
        border: '4px solid',
        borderImage: 'linear-gradient(135deg, #00d4ff, #ff00ff) 1',
        background: isActive
          ? 'linear-gradient(135deg, rgba(0,212,255,0.2), rgba(255,0,255,0.2))'
          : 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: glow,
        opacity,
        transition: 'all 0.3s',
      }}
    >
      <div
        style={{
          fontSize: 48,
          fontWeight: 'bold',
          color: '#fff',
          fontFamily: 'DM Serif Display, serif',
        }}
      >
        {chord}
      </div>
    </div>
  );
};
