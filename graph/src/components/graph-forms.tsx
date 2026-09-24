import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useEco } from "@/lib/store";

const FOG = "#d4cfd9";
const GOLD = "#c9a45c";
const CYAN = "#7ec8d4";
const SILVER = "#c5cdd6";
const INK = "#2a2e38";

function noRay() {}

function helixCurve(radius: number, height: number, turns: number, phase: number) {
  const pts: THREE.Vector3[] = [];
  const n = 72;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const a = t * Math.PI * 2 * turns + phase;
    pts.push(new THREE.Vector3(Math.cos(a) * radius, (t - 0.5) * height, Math.sin(a) * radius));
  }
  return new THREE.CatmullRomCurve3(pts);
}

export function Atmosphere() {
  const reduceMotion = useEco((s) => s.reduceMotion);
  const gold = useMemo(() => new THREE.Color("#e8d7b0"), []);
  const cyan = useMemo(() => new THREE.Color("#c5d8e4"), []);
  const mist = useMemo(() => new THREE.Color(FOG), []);
  const mix = useMemo(() => new THREE.Color(FOG), []);

  useFrame(({ clock, scene }) => {
    const u = reduceMotion ? 0.45 : 0.5 + 0.5 * Math.sin(clock.elapsedTime * 0.11);
    mix.copy(mist).lerp(gold, u * 0.38).lerp(cyan, (1 - u) * 0.32);
    const fog = scene.fog as THREE.Fog | null;
    if (fog) fog.color.copy(mix);
    scene.background = mix;
  });

  return (
    <>
      <color attach="background" args={[FOG]} />
      <fog attach="fog" args={[FOG, 12, 38]} />
      <hemisphereLight args={["#f4eef6", "#b7c4cc", 0.9]} />
      <ambientLight intensity={0.5} />
      <pointLight position={[0, 1.1, 0]} intensity={1.5} color="#ffe6b8" distance={16} />
      <pointLight position={[3.2, 2.4, -2]} intensity={0.7} color="#9fd4e8" distance={14} />
      <directionalLight position={[8, 10, 6]} intensity={0.48} color="#fff4ea" />
    </>
  );
}

export function Helices() {
  const reduceMotion = useEco((s) => s.reduceMotion);
  const group = useRef<THREE.Group>(null);
  const geos = useMemo(
    () => [
      new THREE.TubeGeometry(helixCurve(1.42, 3.6, 2.15, 0), 72, 0.048, 8, false),
      new THREE.TubeGeometry(helixCurve(1.58, 3.4, 2.15, 2.1), 72, 0.042, 8, false),
      new THREE.TubeGeometry(helixCurve(1.74, 3.2, 2.15, 4.2), 72, 0.038, 8, false),
    ],
    [],
  );

  useFrame((_, dt) => {
    if (reduceMotion || !group.current) return;
    group.current.rotation.y += Math.min(dt, 0.1) * 0.12;
  });

  const colors = [GOLD, SILVER, INK];
  return (
    <group ref={group} position={[0, 0.35, 0]}>
      {geos.map((geom, i) => (
        <mesh key={i} geometry={geom} raycast={noRay}>
          <meshStandardMaterial
            color={colors[i]}
            emissive={colors[i]}
            emissiveIntensity={i === 2 ? 0.04 : 0.22}
            metalness={0.55}
            roughness={0.28}
          />
        </mesh>
      ))}
    </group>
  );
}

export function FilamentHalo() {
  const reduceMotion = useEco((s) => s.reduceMotion);
  const mat = useMemo(
    () =>
      new THREE.MeshBasicMaterial({
        color: CYAN,
        wireframe: true,
        transparent: true,
        opacity: 0.18,
        depthWrite: false,
      }),
    [],
  );
  const inner = useMemo(
    () =>
      new THREE.MeshPhysicalMaterial({
        color: "#dfeaf0",
        transparent: true,
        opacity: 0.12,
        roughness: 0.08,
        metalness: 0.15,
        transmission: 0.7,
        thickness: 0.4,
        depthWrite: false,
      }),
    [],
  );

  useFrame(({ clock }) => {
    if (reduceMotion) return;
    const u = 0.14 + 0.08 * (0.5 + 0.5 * Math.sin(clock.elapsedTime * 0.7));
    mat.opacity = u;
  });

  return (
    <group position={[0, 0.35, 0]}>
      <mesh raycast={noRay} material={inner}>
        <sphereGeometry args={[1.05, 32, 24]} />
      </mesh>
      <mesh raycast={noRay} material={mat} scale={1.22}>
        <icosahedronGeometry args={[1, 1]} />
      </mesh>
    </group>
  );
}

const SLABS: { pos: [number, number, number]; rot: [number, number, number]; size: [number, number, number] }[] = [
  { pos: [2.6, 0.8, -1.4], rot: [0.15, 0.7, -0.08], size: [1.1, 1.6, 0.08] },
  { pos: [-2.8, 0.2, 1.1], rot: [-0.2, -0.5, 0.1], size: [0.9, 1.4, 0.07] },
  { pos: [0.4, -1.5, 2.2], rot: [0.4, 0.2, 0], size: [1.4, 0.12, 1.4] },
];

export function GlassSlabs() {
  return (
    <group>
      {SLABS.map((s, i) => (
        <mesh key={i} position={s.pos} rotation={s.rot} raycast={noRay}>
          <boxGeometry args={s.size} />
          <meshPhysicalMaterial
            color={i === 2 ? "#cfe6ee" : "#d8c8e8"}
            transparent
            opacity={0.22}
            roughness={0.08}
            metalness={0.25}
            transmission={0.55}
            thickness={0.35}
            depthWrite={false}
          />
        </mesh>
      ))}
    </group>
  );
}

export function SovereignBeam() {
  const geom = useMemo(() => {
    const curve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-11, -5.5, -6),
      new THREE.Vector3(-4, -1.2, -2),
      new THREE.Vector3(0.2, 0.4, 0.4),
      new THREE.Vector3(5, 2.6, 3),
      new THREE.Vector3(12, 7.2, 7),
    ]);
    return new THREE.TubeGeometry(curve, 64, 0.035, 6, false);
  }, []);
  const reduceMotion = useEco((s) => s.reduceMotion);
  const mat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: GOLD,
        emissive: GOLD,
        emissiveIntensity: 0.55,
        transparent: true,
        opacity: 0.7,
        depthWrite: false,
      }),
    [],
  );
  useFrame(({ clock }) => {
    if (reduceMotion) return;
    mat.emissiveIntensity = 0.4 + 0.35 * (0.5 + 0.5 * Math.sin(clock.elapsedTime * 1.1));
  });
  return <mesh geometry={geom} material={mat} raycast={noRay} />;
}

export function DriftEmbers() {
  const quality = useEco((s) => s.quality);
  const reduceMotion = useEco((s) => s.reduceMotion);
  const count = quality === "alta" ? 42 : 18;
  const mesh = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const seeds = useMemo(
    () =>
      Array.from({ length: 42 }, (_, i) => ({
        x: ((i * 37) % 17) - 8,
        y: ((i * 13) % 11) - 5,
        z: ((i * 19) % 15) - 7,
        s: 0.035 + (i % 6) * 0.008,
        p: i * 0.37,
      })),
    [],
  );

  useFrame(({ clock }) => {
    const inst = mesh.current;
    if (!inst) return;
    const t = reduceMotion ? 0 : clock.elapsedTime;
    for (let i = 0; i < count; i++) {
      const s = seeds[i];
      dummy.position.set(
        s.x + Math.sin(t * 0.17 + s.p) * 0.55,
        ((s.y + t * 0.22 + s.p) % 10) - 5,
        s.z + Math.cos(t * 0.14 + s.p) * 0.45,
      );
      dummy.scale.setScalar(s.s);
      dummy.updateMatrix();
      inst.setMatrixAt(i, dummy.matrix);
    }
    inst.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={mesh} args={[undefined, undefined, count]} raycast={noRay}>
      <sphereGeometry args={[1, 8, 8]} />
      <meshBasicMaterial color="#f0e0b8" transparent opacity={0.55} depthWrite={false} />
    </instancedMesh>
  );
}

export function OrbitingGold() {
  const reduceMotion = useEco((s) => s.reduceMotion);
  const light = useRef<THREE.PointLight>(null);
  useFrame(({ clock }) => {
    if (!light.current || reduceMotion) return;
    const t = clock.elapsedTime * 0.22;
    light.current.position.set(Math.cos(t) * 4.2, 1.4 + Math.sin(t * 0.7) * 0.6, Math.sin(t) * 4.2);
  });
  return <pointLight ref={light} intensity={0.85} color="#ffd9a0" distance={12} position={[4, 1.4, 0]} />;
}
