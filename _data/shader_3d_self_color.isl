in {
	vec4 user_self_color = vec4(1.0,1.0,1.0,1.0);
}

variant {
	vertex {
		out {
			vec2 v_uv;
			vec3 v_normal;
		}

		source %{
			v_uv = vUV0;
			v_normal = vNormal;
		%}
	}

	pixel {
		source %{
			%constant% = user_self_color.xyz;
			%normal% = normalize(v_normal);
		%}
	}
}
