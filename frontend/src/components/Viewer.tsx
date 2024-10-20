import { useStore } from '@/lib/state';
import { getModelUrl } from '@/lib/util';
import { Bounds, Center, OrbitControls } from '@react-three/drei';
import { Canvas, useLoader } from '@react-three/fiber';
import { Suspense } from 'react';
import { STLLoader } from 'three-stdlib';

function LoadingIndicator() {
    return (
        <div className="flex h-full flex-col items-center justify-center">
            <div className="h-24 w-24 animate-spin rounded-full border-r-2 border-emerald-500"></div>
        </div>
    );
}

function ViewerCanvas() {
    const options = useStore((state) => state.modelOptions);

    const stl = useLoader(STLLoader, getModelUrl(options));

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

export function Viewer() {
    return (
        <Suspense fallback={<LoadingIndicator />}>
            <ViewerCanvas />
        </Suspense>
    );
}
