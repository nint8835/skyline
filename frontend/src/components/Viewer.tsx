import { useStore } from '@/lib/state';
import { Bounds, CameraControls, Center, useBounds } from '@react-three/drei';
import { Canvas, useLoader } from '@react-three/fiber';
import { Suspense, useEffect, useRef, useState } from 'react';
import { Mesh } from 'three';
import { STLLoader } from 'three-stdlib';

function LoadingIndicator() {
    return (
        <div className="flex h-full flex-col items-center justify-center">
            <div className="h-24 w-24 animate-spin rounded-full border-r-2 border-emerald-500"></div>
        </div>
    );
}

function Model() {
    const [hasBound, setHasBound] = useState(false);
    const { selectedYear } = useStore();
    const bounds = useBounds();

    const modelUrl = selectedYear ? `/contributions/model/${selectedYear}` : '/blank.stl';

    const stl = useLoader(STLLoader, modelUrl);
    const meshRef = useRef<Mesh>(null);

    useEffect(() => {
        if (!stl || hasBound || !meshRef.current) {
            return;
        }
        // bounds.moveTo([0, 100, 100]);
        // bounds.refresh().clip().fit();
        setHasBound(true);
    }, [stl]);

    return (
        <mesh
            geometry={stl}
            castShadow
            receiveShadow
            rotation={[-Math.PI / 2, 0, -Math.PI / 2]}
            position={[-78, 0, 0]}
            ref={meshRef}
        >
            <meshStandardMaterial />
        </mesh>
    );
}

function ViewerCanvas() {
    return (
        <Canvas shadows>
            {/* <PerspectiveCamera makeDefault /> */}
            {/* <OrbitControls makeDefault /> */}
            <CameraControls makeDefault />
            <Bounds>
                <Center>
                    <Model />
                </Center>
            </Bounds>

            <ambientLight intensity={0.25} />
            <directionalLight position={[-1, 5, -1]} intensity={1} />
        </Canvas>
    );
}

export function Viewer() {
    return (
        <Suspense fallback={<LoadingIndicator />}>
            <ViewerCanvas />
        </Suspense>
    );
}
