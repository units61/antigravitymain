# Directive: Prompt Understanding (Design DNA Extraction)

## 1. Objective
Analyze a raw, unformatted user prompt to extract its core aesthetic intent, brand strategy, and interaction properties. Resolve these intents into a structured `Design DNA` JSON object that maps perfectly to our internal Design Ontology.

---

## 2. Structured DNA Schema

The returned value MUST be a clean, valid JSON object matching the following structure:

```json
{
  "brand_archetype": "string",
  "core_emotion": "string",
  "visual_density": "string",
  "motion_energy": 5,
  "primary_colors": ["string"],
  "target_audience": "string",
  "keywords": ["string"],
  "spatial_depth": "string (near | mid | far | infinite)",
  "camera_movement_style": "string (pan | orbit | dive | zoom | static)",
  "shader_type": "string (fluid | glass | neon-glitch | particle-smoke | water-gold)",
  "required_3d_models": ["string"]
}
```

---

## 3. Detailed Parameter Specifications

### 3.1 Brand Archetype
Map the brand's core identity to exactly **one** of Carl Jung's 12 archetypes:
* **Creator**: Imaginative, innovative, expressive (e.g., Apple, Adobe).
* **Ruler**: High-status, elite, organized, authoritative (e.g., Rolex, Mercedes).
* **Rebel**: Bold, disruptive, revolutionary, uncompromising (e.g., Harley-Davidson, Diesel).
* **Magician**: Transformative, cinematic, visionary (e.g., Disney, Tesla).
* **Innocent**: Wholesome, pure, simple, optimistic (e.g., Dove, Method).
* **Explorer**: Organic, adventurous, raw, independent (e.g., Patagonia, Jeep).
* **Sage**: Analytical, data-heavy, wisdom-driven (e.g., Google, BBC).
* **Jester**: Highly playful, fun-loving, energetic (e.g., Mailchimp, Old Spice).
* **Lover**: Sensual, elegant, intimate, high aesthetic (e.g., Chanel, Gucci).
* **Caregiver**: Nurturing, warm, protective, supportive (e.g., Volvo).
* **Everyman**: Down-to-earth, supportive, authentic (e.g., IKEA, Levi's).
* **Hero**: Determined, courageous, strong, highly kinetic (e.g., Nike, Red Bull).

### 3.2 Core Emotion Mappings
Extract the dominant feeling the digital experience should evoke:
* `luxury` | `calm` | `aggressive` | `playful` | `mysterious` | `trustworthy` | `energetic` | `cyberpunk` | `editorial` | `avant-garde`

### 3.3 Visual Density Guidelines
* `low`: Minimalist, high empty whitespace, spacious (Luxury, Calm).
* `medium`: Balanced, clean, structured grid system (Trustworthy, Editorial).
* `high`: Highly packed, full grid borders, dense textual information (Brutalist, Cyberpunk).

### 3.4 Motion Energy Index
Assign an animation budget rating from **1 to 10**:
* **1-3**: Near-static. Extremely slow-burn, minimal fading.
* **4-6**: Standard responsive. Micro-interactions on buttons, slow cinematic entrance cascades.
* **7-8**: Highly kinetic. Parallax scroll triggers, cursor-following warps, reactive physical bounces.
* **9-10**: Hyper-kinetic/Awwwards level. Constant animation loops, physics engines, full dynamic transitions.

### 3.5 3D Spatial Parameters
* **spatial_depth**: Depth scale of the 3D scene.
  * `near`: Shallow focus, objects close to screen.
  * `mid`: Balanced focus depth.
  * `far`: Deep canvas, objects receding into distance.
  * `infinite`: Skyboxes, infinite starfields, endless horizons.
* **camera_movement_style**: Camera behavior as the user scrolls or interacts.
  * `pan`: Horizontal/vertical sliding camera (e.g. BMW site).
  * `orbit`: Orbiting rotation around a target model (e.g. Nike site).
  * `dive`: Downward or forward zoom depth dive (e.g. Beyondreel site).
  * `zoom`: Focus-based scaling and magnification.
  * `static`: Fixed perspective.
* **shader_type**: Real-time GLSL visual effects and material shaders.
  * `fluid`: Smooth liquid animations and flow fields.
  * `glass`: High-refraction transparency (e.g. Chaumet, luxury Torus).
  * `neon-glitch`: Snappy chromatic aberration and cyber glows.
  * `particle-smoke`: Volumetric fog or dust flows (e.g. Beyondreel tunnel, gold dust).
  * `water-gold`: Deep dark-blue waters with golden highlights (e.g. Gino Group).
* **required_3d_models**: Array of specific 3D mesh queries to fetch (e.g., `["luxury_yacht"]`, `["katana_sword"]`, `["sneaker"]`, `["sports_car"]`).

---

## 4. Edge Cases & Conflict Resolution
* **Contradictory Prompts** (e.g., *"Luxury brutalist, highly calm but energetic"*): Prioritize **Luxury** over Brutalist. Set Visual Density to `low` but use a high-energy kinetic color accent.
* **Vague Prompts** (e.g., *"Cool site"*): Default to archetype `everyman`, emotion `trustworthy`, density `medium`, and motion `5`.
* **Language Support**: Translate Turkish or other localized terms to the correct standard keywords (e.g., "lüks" -> "luxury", "sakin" -> "calm").

---

## 5. ASLA YAPMA (Negative Constraints)
- **ASLA jenerik ve sıkıcı bir 'Everyman' arketipine varsayılan olarak düşme.** Promptun içinde en ufak bir ipucu varsa, bunu Creator, Rebel, Magician veya Lover gibi yüksek sanatsal arketiplere eşle.
- **ASLA düz, sıradan renkler seçme.** 'red', 'blue', 'green' gibi ana renkler yerine her zaman premium HSL veya hex renk kodları türet.
- **ASLA çelişkili veya anlamsız 3D model istekleri üretme.** Seçilen 3D model, marka arketipi ve temayla tam bir bütünlük içinde olmalıdır (Örn: Lüks saat sitesi için spor araba veya mekanik kılıç yerine premium saat kasası iste).
- **ASLA tüm hareket enerjilerini (motion_energy) ortalama 5 olarak sabitleme.** Sakin siteler için kesinlikle 1-3, asi ve cyber temalar için kesinlikle 8-10 gibi net uç değerler belirle.
- **ASLA spatial_depth ve camera_movement_style parametrelerini 'static' veya 'near' olarak sınırlı bırakma.** Awwwards deneyimi derinlik ve akıcılık gerektirir; mümkün mertebe 'far', 'infinite' ve 'orbit', 'dive' kamera stillerini tercih et.
