surface {
	terrain: true
}

in {
	tex2D diffuse_map = "@data/terrain/island_diff.jpg" [filter: anisotropic];
	tex2D normal_map = "@data/terrain/island_nrm.jpg" [filter: anisotropic];
}

variant {
	pixel {
		source %{
			vec3 normal = texture2D(normal_map, vTerrainUV).xzy;
			normal = normal * 2.0 - 1.0;
			normal.z *= -1.f;
			normal = _mtx_mul(vNormalViewMatrix, normal);

			vec3 diff = texture2D(diffuse_map, vTerrainUV).rgb;

			%diffuse% = diff;
			%normal% = normal;
			%specular% = (1.0 - diff) * 0.2;
			%glossiness% = 0.2;
		%}
	}
}
