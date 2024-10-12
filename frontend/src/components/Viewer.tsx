import { Bounds, Center, OrbitControls } from '@react-three/drei';
import { Canvas, useLoader } from '@react-three/fiber';
import { STLLoader } from 'three-stdlib';

export function Viewer({ year, user }: { year: number; user: string }) {
    const stl = useLoader(STLLoader, `/contributions/model/${user}/${year}`);

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
