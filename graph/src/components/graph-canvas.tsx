import { Suspense, useMemo, useRef, type ComponentRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Line, Html, OrbitControls, useTexture } from "@react-three/drei";
import * as THREE from "three";
import {
  EDGES,
  NODE_MAP,
  NODES,
  type GraphNode,
  type Vec3,
} from "@/lib/graph-data";
import { useEco } from "@/lib/store";
import {
  Atmosphere,
  DriftEmbers,
  FilamentHalo,
  GlassSlabs,
  Helices,
  OrbitingGold,
  SovereignBeam,
} from "@/components/graph-forms";

const RIBBONS: { color: string; pts: Vec3[] }[] = [
  {
    color: "#e8b8c8",
    pts: [
      [-8, -3.2, 4],
      [-4, -1.4, 2.2],
      [0.4, 0.2, 1.4],
      [4.2, 1.6, -0.8],
      [7.5, 0.4, -3.4],
    ],
  },
  {
    color: "#9fd4e0",
    pts: [
      [7.8, 3.4, 3.2],
      [3.4, 2.2, 1.6],
      [-0.6, 0.6, 0.2],
      [-4.6, -1.2, -1.6],
      [-8.2, -2.4, -3],
    ],
  },
  {
    color: "#c8b4e0",
    pts: [
      [-6.4, 3.8, -4],
      [-2.2, 2.4, -2.2],
      [1.4, 0.8, -0.6],
      [5.2, -0.8, 1.8],
      [8, -2.6, 3.4],
    ],
  },
  {
    color: "#f0c8b4",
    pts: [
      [5.6, -3.6, -5],
      [2.2, -2, -2.8],
      [-0.8, -0.4, -0.4],
      [-3.6, 1.6, 2.4],
      [-6.8, 3.2, 4.6],
    ],
  },
];

const SHARDS = [
  { pos: [0.2, 0.6, 0.4] as Vec3, rot: [0.55, 0.7, -0.15] as Vec3, w: 7.4, h: 10.2 },
  { pos: [-1.4, -0.2, 1.1] as Vec3, rot: [-0.4, -0.55, 0.3] as Vec3, w: 6.2, h: 8.6 },
  { pos: [1.8, 0.9, -1.2] as Vec3, rot: [0.2, 1.1, 0.4] as Vec3, w: 5.4, h: 7.8 },
  { pos: [-0.6, 1.4, -0.8] as Vec3, rot: [1.1, 0.2, -0.4] as Vec3, w: 4.8, h: 7.2 },
];

function vec(p: Vec3) {
  return new THREE.Vector3(p[0], p[1], p[2]);
}

function noRay() {}

function Ribbon({ color, pts }: { color: string; pts: Vec3[] }) {
  const geom = useMemo(() => {
    const curve = new THREE.CatmullRomCurve3(pts.map(vec));
    return new THREE.TubeGeometry(curve, 80, 0.11, 10, false);
  }, [pts]);
  return (
    <mesh geometry={geom} raycast={noRay}>
      <meshStandardMaterial
        color={color}
        roughness={0.28}
        metalness={0.08}
        emissive={color}
        emissiveIntensity={0.08}
      />
    </mesh>
  );
}

function Shards() {
  return (
    <group>
      {SHARDS.map((s, i) => (
        <mesh key={i} position={s.pos} rotation={s.rot} raycast={noRay}>
          <planeGeometry args={[s.w, s.h]} />
          <meshPhysicalMaterial
            color="#cfc4ea"
            transparent
            opacity={0.13}
            roughness={0.18}
            metalness={0.04}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      ))}
    </group>
  );
}

function CityBackdrop() {
  const tex = useTexture("/stills/city-wide.jpg");
  tex.colorSpace = THREE.SRGBColorSpace;
  return (
    <mesh position={[0, 3.2, -32]} raycast={noRay}>
      <planeGeometry args={[54, 30]} />
      <meshBasicMaterial map={tex} />
    </mesh>
  );
}

function Pulse({ a, b, offset }: { a: Vec3; b: Vec3; offset: number }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({ clock }) => {
    const t = (clock.elapsedTime * 0.18 + offset) % 1;
    const m = ref.current;
    if (!m) return;
    m.position.set(
      a[0] + (b[0] - a[0]) * t,
      a[1] + (b[1] - a[1]) * t,
      a[2] + (b[2] - a[2]) * t,
    );
    const s = 0.7 + Math.sin(t * Math.PI) * 0.5;
    m.scale.setScalar(s);
  });
  return (
    <mesh ref={ref} raycast={noRay}>
      <sphereGeometry args={[0.055, 10, 10]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.9} />
    </mesh>
  );
}

function GraphNodeMesh({ node }: { node: GraphNode }) {
  const selectedId = useEco((s) => s.selectedId);
  const hoveredId = useEco((s) => s.hoveredId);
  const query = useEco((s) => s.query);
  const typeFilter = useEco((s) => s.typeFilter);
  const select = useEco((s) => s.select);
  const hover = useEco((s) => s.hover);
  const showLabels = useEco((s) => s.showLabels);
  const active = selectedId === node.id;
  const hovered = hoveredId === node.id;
  const q = query.trim().toLowerCase();
  const matchesQuery = !q || node.name.toLowerCase().includes(q) || node.community.toLowerCase().includes(q);
  const matchesType = typeFilter === "all" || node.type === typeFilter;
  const dim = (!matchesQuery || !matchesType) && !active;
  const isCore = node.type === "nucleo";
  const showName = !dim && (hovered || active || (showLabels && (isCore || node.size >= 0.72)));

  const mat = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: node.color,
        emissive: node.color,
        emissiveIntensity: isCore ? 0.45 : 0.22,
        roughness: 0.32,
        metalness: 0.18,
      }),
    [node.color, isCore],
  );

  useFrame((_, dt) => {
    const d = Math.min(dt, 0.1);
    mat.emissiveIntensity = THREE.MathUtils.damp(
      mat.emissiveIntensity,
      active ? 0.85 : hovered ? 0.5 : isCore ? 0.45 : 0.2,
      8,
      d,
    );
    mat.opacity = THREE.MathUtils.damp(mat.opacity, dim ? 0.12 : 1, 8, d);
    mat.transparent = dim;
  });

  const pick = (e: { stopPropagation: () => void }) => {
    e.stopPropagation();
    select(node.id);
  };

  return (
    <group position={node.position}>
      <mesh
        material={mat}
        onPointerDown={pick}
        onClick={pick}
        onPointerOver={(e) => {
          e.stopPropagation();
          hover(node.id);
          document.body.style.cursor = "pointer";
        }}
        onPointerOut={() => {
          hover(null);
          document.body.style.cursor = "auto";
        }}
        scale={active ? 1.18 : hovered ? 1.08 : 1}
      >
        <sphereGeometry args={[node.size * 0.42, 28, 28]} />
      </mesh>
      <mesh visible={false} onPointerDown={pick} onClick={pick}>
        <sphereGeometry args={[Math.max(node.size * 0.85, 0.55), 12, 12]} />
      </mesh>
      {isCore ? (
        <>
          <mesh rotation={[Math.PI / 2, 0, 0]} raycast={noRay}>
            <torusGeometry args={[node.size * 0.62, 0.03, 10, 48]} />
            <meshStandardMaterial color="#c9a45c" emissive="#c9a45c" emissiveIntensity={0.55} metalness={0.7} roughness={0.25} />
          </mesh>
          <mesh raycast={noRay}>
            <sphereGeometry args={[node.size * 0.58, 28, 28]} />
            <meshPhysicalMaterial
              color="#f3e4c0"
              emissive="#c9a45c"
              emissiveIntensity={0.35}
              transparent
              opacity={0.35}
              roughness={0.12}
              metalness={0.2}
              transmission={0.45}
              thickness={0.4}
              depthWrite={false}
            />
          </mesh>
        </>
      ) : null}
      {active ? (
        <mesh raycast={noRay}>
          <sphereGeometry args={[node.size * 0.72, 20, 20]} />
          <meshBasicMaterial color={node.color} transparent opacity={0.12} depthWrite={false} />
        </mesh>
      ) : null}
      {showName ? (
        <Html
          center
          sprite
          pointerEvents="none"
          occlude={false}
          distanceFactor={10}
          zIndexRange={[8, 0]}
          position={[0, node.size * 0.58, 0]}
          style={{ pointerEvents: "none", userSelect: "none" }}
        >
          <div className="node-label">{node.name}</div>
        </Html>
      ) : null}
    </group>
  );
}

function Edges() {
  const selectedId = useEco((s) => s.selectedId);
  return (
    <group>
      {EDGES.map((e) => {
        const a = NODE_MAP[e.source];
        const b = NODE_MAP[e.target];
        if (!a || !b) return null;
        const hot = selectedId === e.source || selectedId === e.target;
        const color = hot ? "#c9a45c" : e.kind === "nucleo" ? "#d4b8c8" : "#b8c4d4";
        return (
          <Line
            key={`${e.source}-${e.target}`}
            points={[a.position, b.position]}
            color={color}
            lineWidth={hot ? 2.2 : 1.15}
            transparent
            opacity={hot ? 0.9 : 0.42}
            raycast={noRay}
          />
        );
      })}
    </group>
  );
}

function Pulses() {
  const reduceMotion = useEco((s) => s.reduceMotion);
  if (reduceMotion) return null;
  const list = EDGES.filter((e) => e.kind === "nucleo" || e.kind === "flujo").slice(0, 10);
  return (
    <group>
      {list.map((e, i) => {
        const a = NODE_MAP[e.source];
        const b = NODE_MAP[e.target];
        if (!a || !b) return null;
        return <Pulse key={`${e.source}-${e.target}`} a={a.position} b={b.position} offset={i * 0.11} />;
      })}
    </group>
  );
}

function CameraRig({ interactive }: { interactive: boolean }) {
  const selectedId = useEco((s) => s.selectedId);
  const autoRotate = useEco((s) => s.autoRotate);
  const reduceMotion = useEco((s) => s.reduceMotion);
  const controlsRef = useRef<ComponentRef<typeof OrbitControls>>(null);
  const target = useMemo(() => new THREE.Vector3(), []);

  useFrame((_, dt) => {
    const d = Math.min(dt, 0.1);
    const controls = controlsRef.current;
    if (!controls) return;
    const node = selectedId ? NODE_MAP[selectedId] : null;
    if (node) {
      target.set(node.position[0], node.position[1], node.position[2]);
      controls.target.lerp(target, 1 - Math.exp(-2.4 * d));
    }
  });

  return (
    <OrbitControls
      ref={controlsRef}
      makeDefault
      enabled={interactive}
      enableDamping
      dampingFactor={0.055}
      autoRotate={autoRotate && !reduceMotion && !selectedId}
      autoRotateSpeed={0.38}
      minDistance={4.2}
      maxDistance={22}
      minPolarAngle={0.35}
      maxPolarAngle={Math.PI * 0.78}
      enablePan={interactive}
    />
  );
}

function Scene({ interactive }: { interactive: boolean }) {
  const quality = useEco((s) => s.quality);
  return (
    <>
      <Atmosphere />
      <Suspense fallback={null}>
        <CityBackdrop />
      </Suspense>
      <Shards />
      <GlassSlabs />
      <SovereignBeam />
      <Helices />
      <FilamentHalo />
      <OrbitingGold />
      {quality === "alta" ? <DriftEmbers /> : null}
      {RIBBONS.map((r, i) => (
        <Ribbon key={i} color={r.color} pts={r.pts} />
      ))}
      <Edges />
      <Pulses />
      {NODES.map((n) => (
        <GraphNodeMesh key={n.id} node={n} />
      ))}
      <CameraRig interactive={interactive} />
    </>
  );
}

export function GraphCanvas({
  interactive,
  onFail,
}: {
  interactive: boolean;
  onFail?: () => void;
}) {
  const quality = useEco((s) => s.quality);
  const reduceMotion = useEco((s) => s.reduceMotion);
  const select = useEco((s) => s.select);

  return (
    <Canvas
      camera={{ position: [0.5, 1.4, 10.6], fov: 42, near: 0.1, far: 90 }}
      dpr={quality === "alta" ? [1, 1.5] : [1, 1]}
      gl={{ antialias: quality === "alta", alpha: false, powerPreference: "default", failIfMajorPerformanceCaveat: false }}
      frameloop={reduceMotion ? "demand" : "always"}
      style={{
        touchAction: "none",
        width: "100%",
        height: "100%",
        pointerEvents: interactive ? "auto" : "none",
      }}
      onPointerMissed={() => select(null)}
      onCreated={({ gl }) => {
        const el = gl.domElement;
        const lost = (ev: Event) => {
          ev.preventDefault();
          onFail?.();
        };
        el.addEventListener("webglcontextlost", lost);
      }}
    >
      <Scene interactive={interactive} />
    </Canvas>
  );
}
