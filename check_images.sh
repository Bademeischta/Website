urls=(
    "https://images.unsplash.com/photo-1632759145351-1d592919f522?q=80&w=2070&auto=format&fit=crop"
    "https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=2070&auto=format&fit=crop"
    "https://images.unsplash.com/photo-1760331840361-d751cfc1becf?q=80&w=2070&auto=format&fit=crop"
    "https://images.unsplash.com/photo-1605450099279-533bd3ce379a?auto=format&fit=crop&w=600&q=80"
    "https://images.unsplash.com/photo-1753717202570-605bcd0eea0d?auto=format&fit=crop&w=600&q=80"
    "https://images.unsplash.com/photo-1570931642143-edb21e87ec3e?q=80&w=2070&auto=format&fit=crop"
)

for url in "${urls[@]}"; do
    code=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' "$url")
    echo "$code : $url"
done
