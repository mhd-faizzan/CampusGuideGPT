export default function NotFound() {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      background: "#212121",
      gap: "16px",
    }}>
      <div style={{ fontSize: "48px" }}>🎓</div>
      <div style={{ fontSize: "22px", fontWeight: 600, color: "#ececec" }}>
        page not found
      </div>
      <div style={{ fontSize: "14px", color: "#8e8ea0" }}>
        this page doesn't exist
      </div>
      <a href="/" style={{
        marginTop: "8px",
        fontSize: "14px",
        color: "#8e8ea0",
        textDecoration: "underline",
        cursor: "pointer",
      }}>
        go back home
      </a>
    </div>
  )
}