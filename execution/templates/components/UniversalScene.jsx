"use client";

import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { ScrollControls, useScroll, Text, Float, Environment, MeshTransmissionMaterial, ContactShadows } from '@react-three/drei';
import * as THREE from 'three';

// 1a. Peachweb-inspired organic wavy 3D particle grid shader
function WavyParticleGrid({ count = 2500 }) {
  const pointsRef = useRef();
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    let i = 0;
    const width = 45;
    const depth = 45;
    const rows = Math.sqrt(count);
    const cols = count / rows;
    
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = (r / rows - 0.5) * width;
        const z = (c / cols - 0.5) * depth;
        pos[i * 3] = x;
        pos[i * 3 + 1] = 0; // calculated in useFrame
        pos[i * 3 + 2] = z;
        i++;
      }
    }
    return pos;
  }, [count]);

  useFrame((state) => {
    if (!pointsRef.current) return;
    const time = state.clock.elapsedTime;
    const posAttr = pointsRef.current.geometry.attributes.position;
    
    for (let i = 0; i < count; i++) {
      const x = posAttr.getX(i);
      const z = posAttr.getZ(i);
      // Fluid wavy calculations
      const y = Math.sin(x * 0.15 + time * 0.6) * Math.cos(z * 0.15 + time * 0.6) * 1.2;
      posAttr.setY(i, y - 2.8);
    }
    posAttr.needsUpdate = true;
    pointsRef.current.rotation.y = time * 0.02;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.07} color="#ffa582" transparent opacity={0.5} sizeAttenuation />
    </points>
  );
}

// 1b. Peachweb-inspired floating refractive glass bubbles
function FloatingBubbles({ count = 10 }) {
  const groupRef = useRef();
  const bubbles = useMemo(() => {
    const items = [];
    for (let i = 0; i < count; i++) {
      items.push({
        position: [
          (Math.random() - 0.5) * 14,
          (Math.random() - 0.5) * 10 - 2,
          (Math.random() - 0.5) * -15 - 5,
        ],
        speed: 0.15 + Math.random() * 0.2,
        scale: 0.3 + Math.random() * 0.7,
      });
    }
    return items;
  }, [count]);

  useFrame((state, delta) => {
    if (!groupRef.current) return;
    groupRef.current.children.forEach((child, idx) => {
      const data = bubbles[idx];
      child.position.y += data.speed * delta;
      // Drift slightly horizontally
      child.position.x += Math.sin(state.clock.elapsedTime * 0.5 + idx) * 0.002;
      if (child.position.y > 6) {
        child.position.y = -6;
      }
      child.rotation.x += 0.002;
      child.rotation.y += 0.003;
    });
  });

  return (
    <group ref={groupRef}>
      {bubbles.map((data, idx) => (
        <mesh key={idx} position={data.position} scale={data.scale}>
          <sphereGeometry args={[1.2, 32, 32]} />
          <MeshTransmissionMaterial 
            backside 
            samples={4} 
            thickness={0.7} 
            roughness={0.08}
            chromaticAberration={0.3} 
            anisotropy={0.2} 
            color="#ffdcc7"
          />
        </mesh>
      ))}
    </group>
  );
}

// 1c. Standard Dynamic Particles System based on environment config
function DynamicParticles({ type = "none" }) {
  const count = type === "none" ? 0 : 400;
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 30; // x
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10; // y
      pos[i * 3 + 2] = (Math.random() - 0.5) * -50; // z (depth)
    }
    return pos;
  }, [count]);

  const pointsRef = useRef();
  const scroll = useScroll();

  useFrame((state) => {
    if (!pointsRef.current) return;
    pointsRef.current.position.z = scroll.offset * 20;
    pointsRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    pointsRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.3;
  });

  if (type === "none") return null;

  let color = "#ffffff";
  if (type === "gold_dust") color = "#b49554"; // Luxury gold
  else if (type === "embers") color = "#ff5500"; // Fire embers
  else if (type === "stars") color = "#00aaff"; // Cyber cyan stars

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.08} color={color} transparent opacity={0.8} sizeAttenuation />
    </points>
  );
}

// 2. Dynamic 3D Model placeholder utilizing premium material shaders
function DynamicModel({ sceneData, cameraPath, onSlashTrigger }) {
  const meshRef = useRef();
  const scroll = useScroll();
  const prevPointer = useRef({ x: 0, y: 0 });
  const swingRotation = useRef({ x: 0, y: 0, z: 0 });
  const lastScrollOffset = useRef(0);

  const { query, material, position = [0, 0, -10], rotation = [0, 0, 0], scale = [1, 1, 1], scrollTrigger = 0.5 } = sceneData;

  useFrame((state, delta) => {
    if (!meshRef.current) return;
    const offset = scroll.offset;

    // Detect if we scrolled past the trigger and trigger screen slash
    if (Math.abs(offset - scrollTrigger) < 0.02 && Math.abs(lastScrollOffset.current - scrollTrigger) >= 0.02) {
      if (onSlashTrigger) {
        onSlashTrigger();
      }
    }
    lastScrollOffset.current = offset;
    
    const activeFactor = Math.max(0, 1 - Math.abs(offset - scrollTrigger) * 3.0);
    
    const pointerX = state.pointer.x;
    const pointerY = state.pointer.y;
    
    const dx = pointerX - prevPointer.current.x;
    const dy = pointerY - prevPointer.current.y;
    
    swingRotation.current.z = THREE.MathUtils.lerp(swingRotation.current.z, -dx * 15.0, delta * 10);
    swingRotation.current.x = THREE.MathUtils.lerp(swingRotation.current.x, dy * 8.0, delta * 10);
    
    prevPointer.current = { x: pointerX, y: pointerY };

    let targetPos = [...position];
    let targetRot = [...rotation];

    const isKatana = query.toLowerCase().includes("katana") || query.toLowerCase().includes("sword");
    if (activeFactor > 0.1 && isKatana) {
      targetPos[0] = THREE.MathUtils.lerp(meshRef.current.position.x, pointerX * 6, delta * 8);
      targetPos[1] = THREE.MathUtils.lerp(meshRef.current.position.y, pointerY * 4, delta * 8);
      targetPos[2] = THREE.MathUtils.lerp(meshRef.current.position.z, position[2] + 4, delta * 8);
      
      targetRot[0] = rotation[0] + swingRotation.current.x;
      targetRot[1] = rotation[1] + pointerX * 1.5;
      targetRot[2] = rotation[2] + swingRotation.current.z + Math.sin(state.clock.elapsedTime * 2) * 0.1;
    } else {
      if (cameraPath === "dive") {
        targetPos[2] = THREE.MathUtils.lerp(meshRef.current.position.z, position[2] + offset * 15, delta * 2.5);
      } else if (cameraPath === "orbit") {
        targetRot[1] = THREE.MathUtils.lerp(meshRef.current.rotation.y, rotation[1] + offset * Math.PI * 2, delta * 2);
      } else {
        targetRot[1] = state.clock.elapsedTime * 0.5;
      }
      targetPos[1] = position[1] + Math.sin(state.clock.elapsedTime * 1.5) * 0.15;
    }

    meshRef.current.position.set(targetPos[0], targetPos[1], targetPos[2]);
    meshRef.current.rotation.set(targetRot[0], targetRot[1], targetRot[2]);
    meshRef.current.scale.setScalar(scale[0] * (0.8 + activeFactor * 0.4));
  });

  const geom = useMemo(() => {
    const q = query.toLowerCase();
    if (q.includes("katana") || q.includes("sword")) {
      return null;
    }
    if (q.includes("yacht") || q.includes("boat")) {
      return <tetrahedronGeometry args={[1.8, 1]} />;
    } else if (q.includes("car") || q.includes("vehicle")) {
      return <boxGeometry args={[2.5, 0.8, 1.2]} />;
    } else if (q.includes("sneaker") || q.includes("shoe")) {
      return <torusGeometry args={[1.2, 0.4, 32, 64]} />;
    }
    return <torusKnotGeometry args={[1, 0.3, 128, 16]} />;
  }, [query]);

  const materialComp = useMemo(() => {
    const mat = material.toLowerCase();
    if (mat === "glass") {
      return (
        <MeshTransmissionMaterial 
          backside 
          samples={4} 
          thickness={1} 
          roughness={0.1}
          chromaticAberration={0.5} 
          anisotropy={0.3} 
          color="#ffffff"
        />
      );
    } else if (mat === "gold") {
      return <meshStandardMaterial color="#b49554" roughness={0.1} metalness={0.9} />;
    } else if (mat === "chrome") {
      return <meshStandardMaterial color="#dddddd" roughness={0.05} metalness={1.0} />;
    } else if (mat === "neon") {
      return <meshBasicMaterial color="#00ffcc" toneMapped={false} />;
    }
    return <meshStandardMaterial color="#ffffff" roughness={0.5} metalness={0.2} />;
  }, [material]);

  const isKatana = query.toLowerCase().includes("katana") || query.toLowerCase().includes("sword");

  return (
    <Float speed={isKatana ? 4.5 : 2.5} rotationIntensity={isKatana ? 1.5 : 0.6} floatIntensity={isKatana ? 1.2 : 0.8}>
      <mesh ref={meshRef} position={position} rotation={rotation} scale={scale}>
        {isKatana ? (
          <group rotation={[0, 0, Math.PI / 4]}>
            <mesh position={[0, 1.2, 0]} castShadow>
              <boxGeometry args={[0.04, 2.4, 0.15]} />
              <meshStandardMaterial color="#e2e8f0" roughness={0.05} metalness={0.95} emissive="#ff007f" emissiveIntensity={0.3} />
            </mesh>
            <mesh position={[0, 1.2, 0.08]} castShadow>
              <boxGeometry args={[0.01, 2.4, 0.02]} />
              <meshBasicMaterial color="#00ffff" toneMapped={false} />
            </mesh>
            <mesh position={[0, 0, 0]} castShadow>
              <cylinderGeometry args={[0.18, 0.18, 0.04, 16]} />
              <meshStandardMaterial color="#ffcc00" roughness={0.2} metalness={0.9} />
            </mesh>
            <mesh position={[0, -0.6, 0]} castShadow>
              <cylinderGeometry args={[0.06, 0.06, 1.2, 16]} />
              <meshStandardMaterial color="#111111" roughness={0.9} />
            </mesh>
            <mesh position={[0, -0.6, 0.02]} castShadow>
              <boxGeometry args={[0.07, 1.0, 0.04]} />
              <meshStandardMaterial color="#ff0055" roughness={0.8} />
            </mesh>
          </group>
        ) : (
          <>
            {geom}
            {materialComp}
          </>
        )}
      </mesh>
    </Float>
  );
}

// 3. Dynamic Typography bound to scrolling Z-axis depth
function KineticText({ sceneData }) {
  const groupRef = useRef();
  const scroll = useScroll();
  const { text, subtitle, position = [0, 0, 0], color = "#ffffff", scrollTrigger = 0.0 } = sceneData;

  useFrame((state, delta) => {
    if (!groupRef.current) return;
    const offset = scroll.offset;
    
    const targetZ = position[2] + offset * 35;
    groupRef.current.position.z = THREE.MathUtils.lerp(groupRef.current.position.z, targetZ, delta * 3);
    
    const distanceFromFocus = Math.abs(groupRef.current.position.z);
    const opacity = Math.max(0, 1 - distanceFromFocus / 15);
    
    groupRef.current.children.forEach(child => {
      if (child.material) {
        child.material.opacity = opacity;
        child.material.transparent = true;
      }
    });
  });

  return (
    <group ref={groupRef} position={[position[0], position[1], position[2]]}>
      <Text fontSize={0.9} color={color} anchorX="center" anchorY="bottom">
        {text}
      </Text>
      {subtitle && (
        <Text fontSize={0.25} position={[0, -0.4, 0]} color="#a3a3a3" anchorX="center" anchorY="top" maxWidth={5} textAlign="center">
          {subtitle}
        </Text>
      )}
    </group>
  );
}

// 4. Main Component mapping the JSON scene state
export default function UniversalScene({ sceneState, children }) {
  const { theme = "luxury", camera = {}, environment = {}, scenes = [] } = sceneState;
  const { path: cameraPath = "dive", speed: cameraSpeed = 1.0, fov = 45 } = camera;
  const { type: envType = "night", particles: particlesType = "none", bg_color = "#02050A" } = environment;

  const [slashActive, setSlashActive] = React.useState(false);
  
  const triggerSlash = React.useCallback(() => {
    setSlashActive(true);
    setTimeout(() => {
      setSlashActive(false);
    }, 700);
  }, []);

  const totalPages = Math.max(4, scenes.length + 1);

  const isPeach = theme === "peach" || theme === "peachweb";
  const bg = isPeach ? "#FFF7F2" : bg_color;

  return (
    <div 
      className={`w-full h-screen overflow-hidden relative transition-transform duration-75 ${slashActive ? 'scale-[1.02] skew-x-[1deg] translate-y-1' : ''}`}
      style={{ backgroundColor: bg, select: 'none' }}
    >
      {/* 3D WebGL Background Canvas */}
      <Canvas 
        camera={{ position: [0, 0, 5], fov }} 
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 0 }}
      >
        <color attach="background" args={[bg]} />
        
        {/* Soft studio/neon lighting setup */}
        <ambientLight intensity={isPeach ? 0.75 : envType === "light" ? 0.6 : 0.2} color={isPeach ? "#ffe9dd" : "#ffffff"} />
        <spotLight 
          position={[0, 15, 0]} 
          intensity={isPeach ? 3.5 : 2.5} 
          color={isPeach ? "#ffa27c" : theme === "luxury" ? "#b49554" : "#ffffff"} 
          angle={0.6} 
          penumbra={1} 
        />
        <directionalLight position={[-10, 10, -5]} intensity={isPeach ? 1.2 : 1} color={isPeach ? "#ffe9dd" : "#ffffff"} />
        
        <Environment preset={isPeach ? "apartment" : envType === "light" ? "apartment" : "night"} />

        {/* If we have external 2D children, we render background elements without scroll controls */}
        {children ? (
          <>
            <WavyParticleGrid />
            <FloatingBubbles />
          </>
        ) : (
          <ScrollControls pages={totalPages} damping={0.25} distance={1.2}>
            {particlesType === "peach_grid" ? (
              <>
                <WavyParticleGrid />
                <FloatingBubbles />
              </>
            ) : (
              <DynamicParticles type={particlesType} />
            )}
            
            {scenes.map((scene, idx) => {
              if (scene.type === "kinetic_typography") {
                return <KineticText key={idx} sceneData={scene} />;
              } else if (scene.type === "3d_model") {
                return <DynamicModel key={idx} sceneData={scene} cameraPath={cameraPath} onSlashTrigger={triggerSlash} />;
              }
              return null;
            })}
          </ScrollControls>
        )}

        <ContactShadows position={[0, -2.5, 0]} opacity={isPeach ? 0.2 : 0.4} scale={20} blur={2.5} far={4} />
      </Canvas>

      {/* Foreground 2D HTML Scrollable Overlay */}
      {children && (
        <div className="absolute inset-0 z-10 overflow-y-auto pointer-events-none">
          <div className="pointer-events-auto w-full h-auto">
            {children}
          </div>
        </div>
      )}

      {/* Fullscreen cut overlay */}
      {slashActive && (
        <div className="absolute inset-0 pointer-events-none z-50 flex items-center justify-center overflow-hidden">
          <div 
            className="w-[150%] h-[6px] bg-gradient-to-r from-transparent via-[#ff007f] to-transparent shadow-[0_0_25px_#ff007f] rotate-[25deg] transform scale-x-0"
            style={{
              animation: 'slashAnim 0.5s cubic-bezier(0.19, 1, 0.22, 1) forwards'
            }}
          />
          <div 
            className="absolute inset-0 bg-[#00ffff]/10 mix-blend-color-dodge pointer-events-none"
            style={{
              animation: 'flashAnim 0.3s ease-out forwards'
            }}
          />
          
          <style>{`
            @keyframes slashAnim {
              0% { transform: scaleX(0) rotate(25deg); opacity: 0; }
              20% { transform: scaleX(1.3) rotate(25deg); opacity: 1; }
              100% { transform: scaleX(1) rotate(25deg); opacity: 0; filter: blur(4px); }
            }
            @keyframes flashAnim {
              0% { opacity: 0.9; }
              100% { opacity: 0; }
            }
          `}</style>
        </div>
      )}

      {/* Floating navigation clues (only for pure 3D scenes) */}
      {!children && (
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/40 text-[10px] tracking-[0.3em] uppercase animate-pulse pointer-events-none z-10">
          Scroll down to experience the blade
        </div>
      )}
    </div>
  );
}
