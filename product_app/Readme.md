# Adobe Image Editor - Flutter Image Editing App

A Flutter app implementing a dark futuristic style design for an advanced image editing interface with real AI-powered features including spatial editing, magic transfer, move-and-remove object manipulation and AI agent mode.

## Setup

### Pre-configured Assets

**Models:**
All required ONNX models have already been added to the `assets/` folder and are ready to use:

- **Segmentation Models**: `assets/masking/mobile_sam_image_encoder.onnx` and `assets/masking/mobile_sam.onnx` (MobileSAM)
- **Depth Estimation**: `assets/depth/depth_anything_v2_vits.onnx` (Depth Anything V2)
- **Colorization**: `assets/ddcolor/model.onnx` and `assets/ddcolor/model.data` (DDColor)
- **Object Removal**: `assets/llama object removal/model_v2.onnx`

These models are pre-loaded and will be automatically used by the app when you run it. No additional setup is required.

### Environment Variables

Create `assets/.env` file with the following content:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** The `.env` file is gitignored. You must create it locally. The app will work without it, but Agent Mode will not function without the Gemini API key.

### Configuring Server Links

If you need to change the API server endpoints (for example, if you're using a different backend server), you can do so directly from within the app:

**Steps to Change Server Links:**

1. Build and run the app using `flutter run`
2. From the **Home Screen**, tap the **Settings button** (gear icon) located in the top-right corner next to the "Adobe Spatia" title
3. In the Settings screen, you'll see text fields for:
   - **API Base URL**: For CosXL API and other feature endpoints (default: `http://adobe.knowhere.site/feature`)
   - **Text Extractor API Base URL**: For text extraction service (default: `http://adobe.knowhere.site/feature`)
   - **Move API Base URL**: For Move/Drag and Drop service (default: `http://adobe.knowhere.site/api/v1`)
4. Update the URLs to point to your server endpoints
5. Tap **Save** to apply the changes

**Note:** The server link changes are persisted locally on the device, so you only need to configure them once. The changes will remain even after closing and reopening the app.

## How to Run

1. Install dependencies:

   ```bash
   flutter pub get
   ```

2. Run the app:

   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── main.dart                          # App entry point with model warmup
├── core/                              # Core functionality and shared code
│   ├── cache/                         # Caching services
│   │   ├── model_cache.dart          # ONNX model caching
│   │   └── processing_cache.dart     # Image processing cache
│   ├── config/                        # Configuration
│   │   ├── app_config.dart           # App configuration (model paths, API URLs)
│   │   └── env.dart                  # Environment variable management
│   ├── isolates/                     # Background processing isolates
│   │   ├── isolate_communication.dart # Isolate message passing
│   │   ├── model_isolate.dart       # Model inference isolate
│   │   └── processing_isolate.dart  # Image processing isolate
│   ├── models/                       # Data models
│   │   ├── edit_state.dart          # Edit state for EXIF metadata
│   │   ├── feature_state_cache.dart # Feature state caching
│   │   ├── image_state.dart         # Image state management with mask support
│   │   ├── mock_models.dart         # Mock data models
│   │   ├── parameter_config.dart    # Parameter configuration
│   │   └── saved_image.dart         # Saved image model
│   ├── providers/                    # Riverpod providers
│   │   └── saved_images_provider.dart # Saved images state provider
│   ├── services/                     # Core services
│   │   ├── base_onnx_service.dart   # Base ONNX service
│   │   ├── blind_watermark_core.dart # Blind watermark core logic
│   │   ├── blind_watermark_service.dart # Blind watermark service
│   │   ├── catalogue_service.dart  # Catalogue/virtual try-on service
│   │   ├── colorization_service.dart # Image colorization service
│   │   ├── cosxl_service.dart      # CosXL API service
│   │   ├── depth_service.dart      # Depth estimation service
│   │   ├── exif_save_service.dart  # EXIF metadata saving
│   │   ├── exif_state_service.dart # EXIF state management
│   │   ├── sam_service.dart        # Segmentation service (MobileSAM)
│   │   ├── saved_images_service.dart # Saved images management
│   │   ├── share_service.dart       # Image sharing service
│   │   └── text_extractor_service.dart # Text extraction from images
│   ├── theme/                        # Theming
│   │   └── app_theme.dart          # Dark/light theme configuration
│   ├── utils/                        # Utility functions
│   │   ├── base64_utils.dart       # Base64 encoding/decoding
│   │   ├── coordinate_utils.dart  # Coordinate transformations
│   │   ├── dct_utils.dart         # DCT utilities for watermarking
│   │   ├── debug_utils.dart       # Debug utilities
│   │   ├── depth_estimator.dart   # Depth estimation utilities
│   │   ├── depth_mask_applier.dart # Depth mask application
│   │   ├── depth_zones.dart       # Depth zone calculations
│   │   ├── image_cache.dart      # Image caching utilities
│   │   ├── image_utils.dart      # Image processing utilities
│   │   ├── mask_utils.dart       # Mask manipulation utilities
│   │   ├── model_loader.dart     # ONNX model loading utilities
│   │   ├── navigation_utils.dart # Navigation helpers
│   │   ├── onnxruntime_impl.dart # ONNX runtime implementation
│   │   ├── onnxruntime_stub.dart # ONNX runtime stub (web)
│   │   ├── progress_tracker.dart # Progress tracking
│   │   ├── snackbar_utils.dart  # Snackbar utilities
│   │   ├── surface_normals.dart # Surface normal calculations
│   │   ├── temp_file_manager.dart # Temporary file management
│   │   ├── tensor_utils.dart   # Tensor manipulation
│   │   └── vector3d.dart       # 3D vector utilities
│   └── widgets/                     # Reusable widgets
│       ├── bottom_pill_nav.dart    # Bottom pill navigation bar
│       ├── edit_feature_row.dart  # Edit feature buttons row
│       ├── editor_gradient_background.dart # Editor background gradient
│       ├── feature_slider_panel.dart # Feature slider panel
│       ├── headers/               # Screen headers
│       │   ├── agent_header.dart  # Agent mode header
│       │   └── editor_header.dart # Editor header
│       ├── image_canvas.dart     # Image canvas widget
│       ├── image_display.dart    # Image display widget
│       ├── liquid_glass_container.dart # Liquid glass effect container
│       ├── liquid_glass_widget.dart # Liquid glass widget
│       ├── loading_overlay.dart  # Loading overlay
│       ├── lottie_loading_widget.dart # Lottie loading animation
│       ├── progressive_loader.dart # Progressive image loader
│       ├── recent_projects_row.dart # Recent projects row
│       ├── ripple_effect.dart    # Ripple effect widget
│       ├── rounded_card.dart     # Reusable rounded card
│       ├── splash_screen.dart    # Splash screen
│       └── toolbar_button.dart   # Toolbar button widget
├── features/                        # Feature modules
│   ├── agent/                      # AI Agent Mode
│   │   ├── agent_orchestrator.dart # Agent orchestration
│   │   ├── models/                # Agent data models
│   │   │   ├── agent_plan.dart   # Agent plan model
│   │   │   ├── agent_step.dart   # Agent step model
│   │   │   └── agent_tool.dart   # Agent tool model
│   │   ├── providers/             # Agent providers
│   │   │   ├── agent_mode_provider.dart # Agent mode state
│   │   │   ├── agent_plan_provider.dart # Agent plan state
│   │   │   └── voice_input_provider.dart # Voice input state
│   │   ├── services/              # Agent services
│   │   │   ├── agent_tools_registry.dart # Agent tools registry
│   │   │   ├── gemini_service.dart # Gemini AI service
│   │   │   └── voice_input_service.dart # Voice input service
│   │   └── widgets/               # Agent widgets
│   │       ├── agent_bottom_nav.dart # Agent bottom navigation
│   │       ├── agent_next_button.dart # Agent next button
│   │       ├── agent_plan_stepper.dart # Agent plan stepper
│   │       └── voice_input_bottom_sheet.dart # Voice input sheet
│   ├
│   ├── editor/                     # Editor
│   │   └── screens/
│   │       └── editor_screen.dart # Main editor screen
│   ├── home/                       # Home screen
│   │   ├── home_screen.dart       # Home screen (legacy)
│   │   ├── screens/
│   │   │   ├── home_screen.dart   # Main home screen
│   │   │   └── video_test_screen.dart # Video test screen
│   │   └── widgets/
│   │       ├── animated_mic_button.dart # Animated mic button
│   │       ├── creative_fab.dart  # Creative FAB
│   │       ├── home_action_button.dart # Home action button
│   │       ├── home_background_gradient.dart # Background gradient
│   │       ├── light_streaks_overlay.dart # Light streaks overlay
│   │       ├── recent_activity_card.dart # Recent activity card
│   │       └── ripple_effect.dart # Ripple effect
│   ├── magic_transfer/             # Magic Transfer feature
│   │   ├── screens/
│   │   │   ├── colourize_screen.dart # Colorization screen
│   │   │   ├── magic_transfer_screen.dart # Magic transfer router
│   │   │   └── scene_screen.dart  # Scene transfer screen
│   │   └── widgets/               # Magic transfer widgets
│   ├── mapping/                    # Image Mapping feature
│   │   ├── screens/
│   │   │   └── image_mapping_screen.dart # Image mapping screen
│   │   └── widgets/               # Mapping widgets
│   └── spatial/                    # Spatial Edit feature
│       ├── screens/
│       │   ├── move_screen.dart   # Move object screen
│       │   ├── remove_screen.dart # Remove object screen
│       │   ├── spatial/          # Spatial sub-screens
│       │   │   ├── focus_content.dart # Focus mode content
│       │   │   └── lighting_content.dart # Lighting mode content
│       │   └── spatial_screen.dart # Main spatial screen
│       └── widgets/               # Spatial widgets
└── services/                       # Top-level services
    ├── model_warmup_service.dart  # Model warmup service
    ├── move_service.dart          # Move object service
    └── remove_direct_service.dart # Direct removal service

assets/
├── placeholder.jpg                 # Main placeholder image
├── thumb1.jpg, thumb2.jpg, thumb3.jpg # Thumbnail images
├── logo and bg/                    # Logo and background assets
│   ├── home_screen_bg.png
│   ├── icon.png
│   ├── logo1.png
│   └── Spatia.png
├── lottie/                         # Lottie animations
│   ├── Loading Dots Blue.json
│   └── Loading Lottie animation.json
├── masking/                        # Segmentation models
│   ├── mobile_sam_image_encoder.onnx # SAM encoder
│   └── mobile_sam.onnx            # SAM decoder
├── depth/                          # Depth estimation model
│   └── depth_anything_v2_vits.onnx # Depth Anything V2
├── ddcolor/                        # Colorization model
│   ├── model.onnx
│   └── model.data
├── llama object removal/          # Object removal model
│   └── model_v2.onnx
└── png/                           # PNG assets (300 files)
```


## App Flow

1. **Splash Screen** → Shows for 2 seconds, then navigates to Home Screen
   - Models are warmed up during splash (SAM and Depth models)
   - Lazy models (Colorization) are warmed up after first frame

2. **Home Screen**:
   - Large "Adobe Spatia" title with overflow menu
   - "New Project" label with large rounded card (tap to select image)
   - Three circular action buttons (Camera, Agent Mode mic, XYZ)
   - "Recent Projects" row with scrollable thumbnails
   - Full bleed design with gradient background

3. **Editor Screen**:
   - Large image preview at top with white background
   - Editor header with back, undo, redo, and save buttons
   - Bottom pill navigation with main features:
     - **Spatial Edit**: Advanced lighting, focus, move, and remove features
     - **Magic Transfer**: Scene transfer and colorization
     - **Search**: Opens Agent Mode
   - Each feature screen has its own specialized UI and controls

## Features

### Spatial Edit

Spatial Edit provides depth-aware image manipulation with advanced lighting, object removal, and object movement capabilities.

#### Lighting Mode

**Subfeatures:**

- **Tunnel Lighting**: Depth-based tunnel lighting effect
  - Parameters: Depth, Intensity (0-200%), Width (5-50%), Softness, Ambient (0-100%)
- **Cone Spotlight**: 3D cone-based spotlight with configurable light source
  - Parameters: Cone Angle (10-100°), Light Position (X, Y, Z), Intensity (0-10x), Background, Falloff
  - Tap to position target or light source
- **Area Spotlighting**: 2D Gaussian-based spotlight
  - Parameters: Spread (10-100%), Depth Tolerance (5-60%), Blur (10-150px), Intensity (50-500%), Background, Falloff
  - Tap to position spotlight center
- **Zone Lighting**: Depth-based zone lighting with per-zone adjustments
  - Configuration: Width (5-80%), Angle (0-360°), Tap to set center
  - Zone Adjustments (per zone: Center, Far, Near):
    - Brightness (-100% to +100%)
    - Contrast (-100% to +100%)
    - Tint (-100% to +100%)
    - Warmth (-100% to +100%)

**Workflow:**

1. Select Lighting mode from Spatial Edit
2. Choose a lighting option
3. For Cone/Area Spotlight, tap on image to position
4. For Zone Lighting, configure zone and tap to set center
5. Adjust parameters using sliders
6. Preview in real-time
7. Save or cancel changes

#### Remove Mode

Remove unwanted objects from images using drawing or automatic masking.

**Subfeatures:**

- **Draw**: Draw directly on image to mark areas for removal
- **Mask**: Use tap-to-select masking (SAM) to automatically select objects

**Workflow:**

1. Select Remove mode from Spatial Edit
2. Choose removal method (Draw or Mask)
3. Mark areas or tap objects to select
4. Process removal
5. Preview result
6. Save or cancel

#### Move Mode

Relocate objects within images while maintaining spatial context.

**Features:**

- **Depth Aware**: Enable depth-aware movement for realistic placement
- **Automatic Selection**: Tap to select objects using SAM
- **Depth Scaling**: Objects automatically scale based on depth differences

**Workflow:**

1. Select Move mode from Spatial Edit
2. Tap object to move (SAM auto-selects)
3. Tap destination location
4. Optionally enable/disable depth-aware mode
5. Preview result
6. Save or cancel

### Magic Transfer

Transform images using AI-powered scene transfer, object manipulation, and colorization.

#### Scene Mode

Transfer style or ambiance using text prompts or reference images.

**Subfeatures:**

- **Via Text Prompt**:
  - With Masking (Apply to Object/Background)
  - Without Masking
- **Via Reference Image**:
  - With Masking (Apply to Object/Background)
  - Without Masking
  - Auto-extracts prompt from reference image

**Workflow:**

1. Select Scene mode
2. Choose input method (Text or Reference Image)
3. Optionally enable masking and choose apply mode
4. Tap "Transfer Scene" to apply
5. Preview result
6. Save or cancel

#### Recolor Mode

AI-powered colorization with optional masking support.

**Subfeatures:**

- With Masking (colorize specific areas)
- Without Masking (colorize entire image)

**Workflow:**

1. Select Recolor mode
2. Optionally enable masking and tap to create mask
3. Tap "Colorize Image" or "Colorize Masked Area"
4. Preview result
5. Save or cancel

### Agent Mode

AI-powered editing assistant that understands natural language commands and orchestrates complex editing workflows.

**Features:**

- **Voice Input**: Speak your editing requests
- **Text Input**: Type your editing requests
- **Plan Generation**: AI generates step-by-step editing plan
- **Automatic Execution**: Executes plan steps automatically
- **Tool Registry**: Supports all editing tools (lighting, remove, move, colorize, etc.)

**Workflow:**

1. Select an image on home screen
2. Tap Agent Mode button (mic icon)
3. Speak or type your editing request
4. AI generates a plan
5. Review plan steps
6. Navigate through steps using Next/Back buttons
7. Each step applies automatically
8. Complete workflow or exit Agent Mode

**Supported Tools:**

- `relight` - Apply lighting effects (tunnel, cone, area, zone)
- `remove` - Remove objects
- `move` - Move objects
- `colorize` - Colorize images
- `scene_transfer` - Transfer scene style
- And more...

### Image Mapping

Map images with various transformation capabilities.

**Features:**

- Image transformation and mapping
- Customizable mapping parameters

## Design Notes

- **Theme**: Dark futuristic iOS-style design
- **Colors**:
  - Background: `#0B0B0B`
  - Card/Panel: `#292A2C` / `#38383A`
  - Muted gray: `#9B9B9B`
  - Accent blue: `#2F82FF`
  - Soft white: `#F3F3F3`
- **Animations**: 250-350ms duration with `Curves.easeInOut`
- **AI Processing**: Real-time image processing using ONNX models and API endpoints
- **Liquid Glass Effects**: Modern glassmorphism UI elements

## Technical Details

### Image Processing

- **ONNX Runtime**: Uses ONNX Runtime for model inference
- **API Endpoints**: Some features use API endpoints (inpainting, scene transfer, colorization)
- **Isolates**: Heavy processing runs in background isolates to maintain UI responsiveness
- **Caching**: Models and depth maps are cached for performance

### Models

- **MobileSAM**: Segmentation (Segment Anything Model)
- **Depth Anything V2**: Depth estimation
- **DDColor**: Image colorization
- **Llama Object Removal**: Object removal

### State Management

- **Riverpod**: Used for state management (saved images, agent mode, agent plan)
- **Singleton Pattern**: Image state uses singleton pattern with mask support
- **Feature State Cache**: Each feature caches its state for save/cancel workflow

### Performance

- **Image Resizing**: Images automatically resized to 1080p max for processing
- **Lazy Loading**: Models loaded lazily on first use
- **Model Warmup**: Startup models (SAM, Depth) warmed up during splash
- **Background Processing**: Heavy operations run in isolates
- **Debounced Updates**: Parameter changes use debouncing for smooth real-time preview

### Navigation

- **Standard Navigator**: Uses Flutter Navigator with hero animations
- **Feature Hierarchy**: Multi-level feature navigation (Spatial Edit → Lighting → Options)
- **Agent Mode Navigation**: Special navigation for agent mode with step-by-step flow

### EXIF Metadata

- **Edit State Saving**: Edit parameters saved to EXIF metadata
- **State Restoration**: Edit state restored when loading images with EXIF data
- **Watermarking**: Blind watermarking applied to saved images


### Responsive Design

- Optimized for common phone sizes (360-430 dp width)
- Adaptive layouts for different screen sizes

## Building

```bash
# Debug build
flutter build apk --debug

# Release build
flutter build apk --release

# iOS build
flutter build ios --release

# Web build (limited - ONNX runtime not fully supported)
flutter build web
```

## Notes

- The app handles missing images and model files gracefully with error builders
- All animations are smooth and performant
- Code is modular and well-commented
- Follows Flutter best practices and null-safety
- ONNX models are loaded lazily on first use
- Image processing happens asynchronously to maintain UI responsiveness
- Mask operations support multiple masks simultaneously
- Undo/redo functionality available for image edits
- Long-press on preview images to view original image
- Features can be stacked - processed images become the base for subsequent edits
- All parameters use debounced updates for smooth real-time preview
- Agent Mode requires Gemini API key in `.env` file
- Web platform has limited support (ONNX runtime FFI not supported)
- EXIF metadata preserves edit history for loaded images

