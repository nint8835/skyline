import { useStore } from '@/lib/state';
import { CameraControls, Environment } from '@react-three/drei';
import { Canvas, useLoader } from '@react-three/fiber';
import { Suspense, useEffect, useRef } from 'react';
import { Group, Sphere } from 'three';
import { STLLoader } from 'three-stdlib';

function LoadingIndicator() {
    return (
        <div className="flex h-full flex-col items-center justify-center">
            <div className="h-24 w-24 animate-spin rounded-full border-r-2 border-emerald-500"></div>
        </div>
    );
}

function Model() {
    const { selectedYear } = useStore();
    const modelUrl = selectedYear ? `/contributions/model/${selectedYear}` : '/blank.stl';
    const stl = useLoader(STLLoader, modelUrl);
    const camControlsRef = useRef<CameraControls>(null);
    const groupRef = useRef<Group>(null);

    useEffect(() => {
        if (camControlsRef.current) {
            console.log('Fitting');
            stl.computeBoundingSphere();
            camControlsRef.current.fitToSphere(stl.boundingSphere as Sphere, false);
        }
    }, [camControlsRef, stl]);

    return (
        <group ref={groupRef}>
            <mesh
                geometry={stl}
                castShadow
                receiveShadow
                rotation={[-Math.PI / 2, 0, -Math.PI / 2]}
                position={[-78, 0, 0]}
            >
                <meshStandardMaterial />
            </mesh>
            <CameraControls ref={camControlsRef} makeDefault />
        </group>
    );
}

function ViewerCanvas() {
    return (
        <Canvas shadows>
            <Model />
            <ambientLight />
            <Environment preset="sunset" />
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
