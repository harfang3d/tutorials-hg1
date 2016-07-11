variant {
	vertex {
		out { vec4 v_color; }

		source %{
			v_color = vColor0;
			%out.position% = vec4(vPosition, 1.0);
		%}
	}

	pixel {
		in { vec4 v_color; }

		source %{
			%out.color% = v_color;
		%}
	}
}
