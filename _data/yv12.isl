in {
	tex2D y_tex;
	tex2D u_tex;
	tex2D v_tex;
}

variant {
	vertex {
		out { vec2 v_uv; }

		source %{
			v_uv = vUV0;
			%out.position% = _mtx_mul(vModelViewProjectionMatrix, vec4(vPosition, 1.0));
		%}
	}

	pixel {
		in { vec2 v_uv; }

		source %{
			#define K 256.0

			float y = texture2D(y_tex, v_uv).x;
			float u = texture2D(u_tex, v_uv).x;
			float v = texture2D(v_tex, v_uv).x;

			vec4 cde = vec4(y - 16.0 / K, vec2(u, v) - 128.0 / K, 1.0);

			mat4 cde_to_rgb = mat4(	298.0 / K, 	0.0,			409.0 / K,		0.0,
									298.0 / K, 	-100.0 / K,		-208.0 / K, 	0.0,
									298.0 / K, 	516.0 / K,		0.0,			0.0,
									0,			0,				0,				1.0);

			%out.color% = clamp(cde * cde_to_rgb, 0.0, 1.0);
		%}
	}
}
