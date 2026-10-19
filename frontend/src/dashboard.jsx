import { useCallback, useEffect, useState } from 'react';
import { api } from './api';

const initialForm = {
  operator: '',
  projekt_name: 'ESD_Test',
  test_art: 'ESD',
  test_point: 'KL30',
  voltage_kv: 1,
  polarity: 'positive',
};

function formatDate(value) {
  return value ? new Date(value).toLocaleString('de-DE') : '—';
}

export default function App({ navigate }) {
  const [form, setForm] = useState(initialForm);
  const [measurements, setMeasurements] = useState([]);
  const [selected, setSelected] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState({ type: '', text: '' });

  const loadMeasurements = useCallback(async () => {
    setLoading(true);
    try {
      setMeasurements(await api.listMeasurements());
      setNotice((current) =>
        current.type === 'error' ? { type: '', text: '' } : current,
      );
    } catch (error) {
      setNotice({
        type: 'error',
        text: `Historie konnte nicht geladen werden: ${error.message}`,
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMeasurements();
  }, [loadMeasurements]);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  /*  async function startMeasurement(event) {
        event.preventDefault();
        setBusy(true);
        setNotice({ type: 'info', text: 'Messung läuft …' });
        try {
        const result = await api.createMeasurement({
            ...form,
            voltage_kv: Number(form.voltage_kv),
        });
        setSelected(result);
        setNotice({
            type: 'success',
            text: `Messung #${result.id} wurde abgeschlossen.`,
        });
        await loadMeasurements();
        } catch (error) {
        setNotice({
            type: 'error',
            text: `Messung fehlgeschlagen: ${error.message}`,
        });
        } finally {
        setBusy(false);
        }
    }
    */
  async function showDetails(id) {
    try {
      setSelected(await api.getMeasurement(id));
    } catch (error) {
      setNotice({
        type: 'error',
        text: `Details konnten nicht geladen werden: ${error.message}`,
      });
    }
  }

  async function removeMeasurement(id) {
    if (!window.confirm(`Messung #${id} wirklich löschen?`)) return;
    try {
      await api.deleteMeasurement(id);
      if (selected?.id === id) setSelected(null);
      setNotice({ type: 'success', text: `Messung #${id} wurde gelöscht.` });
      await loadMeasurements();
    } catch (error) {
      setNotice({
        type: 'error',
        text: `Löschen fehlgeschlagen: ${error.message}`,
      });
    }
  }

  return (
    <main className="shell">
      {notice.text && (
        <div className={`notice ${notice.type}`}>{notice.text}</div>
      )}

      {/*  <section className="grid">
            <form className="panel form-panel" onSubmit={startMeasurement}>
            <div className="section-title">
                <span>01</span>
                <h2>Messung konfigurieren</h2>
            </div>
            <div className="fields">
                <label>
                Projekt
                <input
                    name="projekt_name"
                    value={form.projekt_name}
                    onChange={updateField}
                    required
                />
                </label>
                <label>
                Operator
                <input
                    name="operator"
                    value={form.operator}
                    onChange={updateField}
                    placeholder="Name"
                    required
                />
                </label>
                <label>
                Testart
                <input
                    name="test_art"
                    value={form.test_art}
                    onChange={updateField}
                    required
                />
                </label>
                <label>
                Testpunkt
                <input
                    name="test_point"
                    value={form.test_point}
                    onChange={updateField}
                    required
                />
                </label>
                <label>
                Spannung [kV]
                <input
                    name="voltage_kv"
                    type="number"
                    step="0.1"
                    value={form.voltage_kv}
                    onChange={updateField}
                    required
                />
                </label>
                <label>
                Polarität
                <select
                    name="polarity"
                    value={form.polarity}
                    onChange={updateField}
                >
                    <option value="positive">Positiv</option>
                    <option value="negative">Negativ</option>
                </select>
                </label>
            </div>
            <button className="primary" disabled={busy}>
                {busy ? 'Messung läuft …' : 'Messung starten'}
            </button>
            </form>

            <section className="panel result-panel">
            <div className="section-title">
                <span>02</span>
                <h2>Ergebnis</h2>
            </div>
            {selected ? (
                <div className="result-content">
                <div className="metrics">
                    <div>
                    <small>Messwert</small>
                    <strong>
                        {selected.measured_voltage} <em>V</em>
                    </strong>
                    </div>
                    <div>
                    <small>Status</small>
                    <strong className="status-value">{selected.status}</strong>
                    </div>
                </div>
                <dl>
                    <div>
                    <dt>ID</dt>
                    <dd>#{selected.id}</dd>
                    </div>
                    <div>
                    <dt>Scope</dt>
                    <dd>{selected.scope_name}</dd>
                    </div>
                    <div>
                    <dt>Zeit</dt>
                    <dd>{formatDate(selected.created_at)}</dd>
                    </div>
                </dl>
                <a
                    className="image-frame"
                    href={api.screenshotUrl(selected.id)}
                    target="_blank"
                    rel="noreferrer"
                >
                    <img
                    src={`${api.screenshotUrl(selected.id)}?t=${Date.now()}`}
                    alt={`Scope-Aufnahme Messung ${selected.id}`}
                    />
                </a>
                </div>
            ) : (
                <div className="empty">
                Wähle eine Messung aus oder starte eine neue.
                </div>
            )}
            </section>
        </section> */}

      <section className="panel history-panel">
        <div className="history-head">
          <div className="section-title">
            <span>03</span>
            <h2>Messhistorie</h2>
          </div>
          <button
            className="secondary"
            onClick={loadMeasurements}
            disabled={loading}
          >
            ↻ Aktualisieren
          </button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Datum</th>
                <th>Projekt</th>
                <th>Testpunkt</th>
                <th>HW</th>
                <th>Level</th>
                <th>Polarität</th>
                <th>Messwert</th>
                <th>Status</th>
                <th>Aktionen</th>
              </tr>
            </thead>
            <tbody>
              {measurements.map((item) => (
                <tr
                  key={item.id}
                  className={selected?.id === item.id ? 'selected' : ''}
                >
                  <td>#{item.id}</td>
                  <td>{formatDate(item.created_at)}</td>
                  <td>{item.projekt_name}</td>
                  <td>{item.test_point}</td>
                  <td>{item.esd_voltage_kv} kV</td>
                  <td>{item.polarity}</td>
                  <td>{item.hw}</td>
                  <td>{item.measured_voltage} V</td>
                  <td>
                    <span className="badge">{item.status}</span>
                  </td>
                  <td className="actions">
                    <button onClick={() => showDetails(item.id)}>
                      Details
                    </button>
                    <a
                      href={api.screenshotUrl(item.id)}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Bild
                    </a>
                    <button
                      className="danger"
                      onClick={() => removeMeasurement(item.id)}
                    >
                      Löschen
                    </button>
                  </td>
                </tr>
              ))}
              {!loading && measurements.length === 0 && (
                <tr>
                  <td className="no-data" colSpan="10">
                    Noch keine Messungen vorhanden.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
