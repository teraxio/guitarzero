import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

interface TabNote {
  string: number; // 1-6 para guitarra (1=más aguda)
  fret: number;
  startFrame: number;
  duration: number;
}

interface TabViewerProps {
  notes: TabNote[];
  strings?: number; // Default 6 para guitarra
}

export const TabViewer: React.FC<TabViewerProps> = ({notes, strings = 6}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const stringHeight = 60;
  const totalHeight = stringHeight * (strings - 1);

  return (
    <div
      style={{
        width: '100%',
        height: totalHeight + 100,
        position: 'relative',
        padding: '50px',
        background: 'rgba(0,0,0,0.8)',
      }}
    >
      {/* Cuerdas */}
      {Array.from({length: strings}).map((_, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            top: 50 + i * stringHeight,
            left: 50,
            right: 50,
            height: 2,
            background: '#666',
          }}
        />
      ))}

      {/* Notas */}
      {notes.map((note, i) => {
        const isActive =
          frame >= note.startFrame &&
          frame < note.startFrame + note.duration;

        const opacity = isActive ? 1 : 0.3;
        const scale = isActive ? 1.2 : 1;
        const glow = isActive ? '0 0 20px rgba(0,212,255,0.8)' : 'none';

        // Posición horizontal basada en tiempo
        const x = interpolate(
          note.startFrame,
          [0, fps * 10],
          [100, 1000],
          {extrapolateRight: 'clamp'}
        );

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: 50 + (note.string - 1) * stringHeight - 20,
              width: 40,
              height: 40,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #00d4ff, #ff00ff)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              fontWeight: 'bold',
              fontSize: 18,
              opacity,
              transform: `scale(${scale})`,
              boxShadow: glow,
              transition: 'all 0.2s',
            }}
          >
            {note.fret}
          </div>
        );
      })}
    </div>
  );
};
