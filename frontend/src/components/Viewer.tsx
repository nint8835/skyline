import { Bounds, Center, OrbitControls } from '@react-three/drei';
import { Canvas, useLoader } from '@react-three/fiber';
import { Suspense } from 'react';
import { STLLoader } from 'three-stdlib';

function ViewerCanvas({ year }: { year: number }) {
    const stl = useLoader(STLLoader, `/contributions/model/${year}`);

    return (
        <Canvas shadows>
            <OrbitControls makeDefault />
            <Bounds fit clip observe>
                <Center>
                    <mesh geometry={stl} castShadow receiveShadow rotation={[-Math.PI / 2, 0, -Math.PI / 2]}>
                        <meshStandardMaterial />
                    </mesh>
                </Center>
            </Bounds>
            <ambientLight intensity={0.25} />
            <directionalLight position={[-1, 5, -1]} intensity={1} />
        </Canvas>
    );
}

export function Viewer({ year }: { year: number }) {
    return (
        <Suspense fallback={null}>
            <ViewerCanvas key={year} year={year} />{' '}
        </Suspense>
    );
}
