import { Bounds, OrbitControls, PerspectiveCamera, useBounds } from '@react-three/drei';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { Suspense, useRef } from 'react';
import { Mesh, Vector3 } from 'three';
import { STLLoader } from 'three-stdlib';

function Model({ year, user }: { year: number; user: string }) {
    const stl = useLoader(STLLoader, `/contributions/model/${user}/${year}`);
    const bounds = useBounds();
    bounds.refresh().clip().fit();
    const scale = new Vector3(0, 0, 0);
    const meshRef = useRef<Mesh>(null);
    let hasBound = false;

    useFrame(() => {
        scale.lerp(new Vector3(1, 1, 1), 0.1);

        if (!meshRef.current) {
            return;
        }

        if (
            meshRef.current.scale.x > 0.99 &&
            meshRef.current.scale.y > 0.99 &&
            meshRef.current.scale.z > 0.99 &&
            !hasBound
        ) {
            // bounds.refresh().clip().fit();
            hasBound = true;
        }

        meshRef.current.scale.copy(scale);
    });

    return (
        <mesh ref={meshRef}>
            <mesh
                geometry={stl}
                castShadow
                receiveShadow
                rotation={[-Math.PI / 2, 0, -Math.PI / 2]}
                position={[-78, 0, 0]}
            >
                <meshStandardMaterial />
            </mesh>
        </mesh>
    );
}

function ViewerCanvas({ year, user }: { year: number; user: string }) {
    return (
        <Canvas shadows>
            <PerspectiveCamera makeDefault position={[0, 0, 100]} />
            <OrbitControls makeDefault />
            <Bounds>
                {/* <Center> */}
                <Model year={year} user={user} />
                {/* </Center> */}
            </Bounds>
            <ambientLight intensity={0.25} />
            <directionalLight position={[-1, 5, -1]} intensity={1} />
        </Canvas>
    );
}

export function Viewer({ year, user }: { year: number; user: string }) {
    return (
        <Suspense fallback={null}>
            <ViewerCanvas year={year} user={user} />
        </Suspense>
    );
}
