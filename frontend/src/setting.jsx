export default function Setting({ navigate }) {
  return (
    <div className="dashboard">
      <h2>Setting</h2>
      <p>This is the setting page.</p>
      <button type="button" onClick={() => navigate('/')}>
        Back to measurement console
      </button>
    </div>
  );
}
