in { tex2D u_tex;
     mat4 persp_mat;}

variant {
	vertex {
		out { vec2 v_uv; }

		source %{
			v_uv = vUV0;
			%out.position% = _mtx_mul(persp_mat, vec4(vPosition, 1.0));
		%}
	}

	pixel {
		in { vec2 v_uv; }

		source %{
			%out.color% = texture2D(u_tex, v_uv);
		%}
	}
}
