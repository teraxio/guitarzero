import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {GZBRBranding} from '../components/GZBRBranding';
import {TabViewer} from '../components/TabViewer';

export const SevenNationArmy: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Riff icónico: E-E-G-E-D-C-B (cuerda A de bajo)
  const riffTabs = [
    // Primera frase
    {string: 4, fret: 7, startFrame: fps * 3, duration: fps * 0.5},
    {string: 4, fret: 7, startFrame: fps * 3.5, duration: fps * 0.5},
    {string: 4, fret: 10, startFrame: fps * 4, duration: fps * 0.75},
    {string: 4, fret: 7, startFrame: fps * 4.75, duration: fps * 0.5},
    {string: 4, fret: 5, startFrame: fps * 5.25, duration: fps * 0.5},
    {string: 4, fret: 3, startFrame: fps * 5.75, duration: fps * 0.5},
    {string: 4, fret: 2, startFrame: fps * 6.25, duration: fps * 1},
    
    // Repetición
    {string: 4, fret: 7, startFrame: fps * 7.5, duration: fps * 0.5},
    {string: 4, fret: 7, startFrame: fps * 8, duration: fps * 0.5},
    {string: 4, fret: 10, startFrame: fps * 8.5, duration: fps * 0.75},
    {string: 4, fret: 7, startFrame: fps * 9.25, duration: fps * 0.5},
    {string: 4, fret: 5, startFrame: fps * 9.75, duration: fps * 0.5},
    {string: 4, fret: 3, startFrame: fps * 10.25, duration: fps * 0.5},
    {string: 4, fret: 2, startFrame: fps * 10.75, duration: fps * 1.5},
  ];

  // Calcular intensidad de la nota actual para efectos visuales
  const getCurrentIntensity = () => {
    const activeNote = riffTabs.find(
      (note) => frame >= note.startFrame && frame < note.startFrame + note.duration
    );
    return activeNote ? 1 : 0;
  };

  const intensity = getCurrentIntensity();

  return (
    <AbsoluteFill style={{background: '#0a0e12'}}>
      {/* Intro */}
      <Sequence from={0} durationInFrames={fps * 3}>
        <GZBRBranding text="Bass Tutorial" />
      </Sequence>

      {/* Tutorial principal */}
      <Sequence from={fps * 3}>
        <AbsoluteFill>
          {/* Fondo pulsante */}
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: `radial-gradient(circle at center, rgba(0,212,255,${intensity * 0.3}), transparent)`,
              transition: 'all 0.1s',
            }}
          />

          {/* Título */}
          <div
            style={{
              position: 'absolute',
              top: 40,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontSize: 56,
              color: '#fff',
              fontFamily: 'DM Serif Display, serif',
              textShadow: '0 0 20px rgba(0,212,255,0.8)',
            }}
          >
            Seven Nation Army
          </div>

          {/* Subtítulo */}
          <div
            style={{
              position: 'absolute',
              top: 120,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontSize: 24,
              color: '#00d4ff',
            }}
          >
            The White Stripes - Bass Riff
          </div>

          {/* Notación de notas */}
          <div
            style={{
              position: 'absolute',
              top: 200,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontSize: 48,
              color: '#fff',
              fontFamily: 'monospace',
              letterSpacing: 20,
            }}
          >
            E - E - G - E - D - C - B
          </div>

          {/* Tabs */}
          <div style={{position: 'absolute', top: 300, left: 0, right: 0}}>
            <TabViewer notes={riffTabs} strings={4} />
          </div>

          {/* Tempo indicator */}
          <div
            style={{
              position: 'absolute',
              top: 700,
              left: 0,
              right: 0,
              textAlign: 'center',
              fontSize: 32,
              color: '#ff00ff',
            }}
          >
            ♩ = 120 BPM
          </div>

          {/* Progress bar */}
          <div
            style={{
              position: 'absolute',
              bottom: 20,
              left: 50,
              right: 50,
              height: 6,
              background: 'rgba(255,255,255,0.2)',
              borderRadius: 3,
            }}
          >
            <div
              style={{
                width: `${(frame / (fps * 20)) * 100}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #00d4ff, #ff00ff)',
                borderRadius: 3,
                boxShadow: '0 0 10px rgba(0,212,255,0.8)',
              }}
            />
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* Outro */}
      <Sequence from={fps * 17} durationInFrames={fps * 3}>
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
                fontSize: 72,
                color: '#000',
                fontFamily: 'DM Serif Display, serif',
                margin: 0,
              }}
            >
              ¡Perfecto!
            </h2>
            <div style={{fontSize: 36, color: '#000', marginTop: 30}}>
              Sigue practicando en BandLoop™
            </div>
            <div
              style={{
                fontSize: 24,
                color: '#000',
                marginTop: 20,
                opacity: 0.8,
              }}
            >
              guitarzero.com
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
