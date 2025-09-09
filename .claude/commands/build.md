# /build - Intelligent Project Builder Command

## Purpose
Framework-aware project building with automatic detection, optimization, and quality validation.

## Usage
```
/build [target] [--options]
```

## Build Types

### Auto-Detection Builds
- `/build` - Detect framework and build entire project
- `/build --analyze` - Analyze build configuration and suggest optimizations
- `/build --watch` - Continuous build with file watching
- `/build --production` - Production-optimized build with validation

### Targeted Builds  
- `/build frontend --optimize bundle` - Frontend-specific build
- `/build api --test` - API build with automated testing
- `/build docs --deploy` - Documentation build and deployment
- `/build component ButtonComponent` - Single component build

### Framework-Specific
- `/build react --bundle-analysis` - React with webpack bundle analyzer
- `/build nextjs --edge` - Next.js with edge deployment
- `/build vue --pwa` - Vue.js with PWA features
- `/build node --docker` - Node.js with containerization

## Framework Detection Engine

### Auto-Detection Patterns
```yaml
React/Next.js:
  indicators: [package.json→react, next.config.js, pages/, app/]
  build_command: npm run build / yarn build
  optimization: bundle analysis, code splitting
  
Vue/Nuxt:
  indicators: [package.json→vue, nuxt.config.js, layouts/, pages/]
  build_command: npm run build / yarn build  
  optimization: treeshaking, lazy loading

Node.js/Express:
  indicators: [package.json→express, server.js, app.js, routes/]
  build_command: npm run build / tsc
  optimization: minification, clustering

Python/Django:
  indicators: [requirements.txt, manage.py, settings.py]
  build_command: python manage.py collectstatic
  optimization: static file compression

Go:
  indicators: [go.mod, main.go, cmd/]
  build_command: go build
  optimization: binary size reduction, cross-compilation
```

### Multi-Framework Projects
- Detects monorepo structures (lerna, nx, rush)
- Builds dependencies in correct order
- Optimizes shared dependencies and build caching
- Coordinates frontend/backend build processes

## Intelligence Layers

### Wave Orchestration (Auto-activates: complex builds + optimization)
- **Progressive Building**: Multi-stage builds with validation checkpoints
- **Systematic Optimization**: Methodical performance and bundle analysis  
- **Adaptive Configuration**: Dynamic build settings based on project characteristics
- **Enterprise Scaling**: Large-scale builds with parallel processing

### MCP Server Integration
- **Magic** (Primary): UI component builds, design system integration
- **Context7** (Secondary): Framework best practices and build patterns
- **Sequential** (Complex): Multi-step build orchestration and analysis
- **Playwright** (Validation): E2E testing and build verification

### Persona Auto-Activation
- **Frontend**: UI builds, component libraries, PWA features
- **Backend**: API builds, containerization, deployment optimization  
- **DevOps**: CI/CD integration, deployment automation, monitoring setup
- **Performance**: Bundle analysis, optimization strategies, caching

## Build Optimization Strategies

### Performance Optimization
- **Bundle Analysis**: Identify large dependencies and optimization opportunities
- **Code Splitting**: Implement intelligent lazy loading and dynamic imports
- **Tree Shaking**: Remove unused code and dependencies
- **Compression**: Gzip/Brotli compression and asset optimization
- **Caching**: Build caching, CDN configuration, service worker setup

### Quality Integration
- **Pre-Build Validation**: TypeScript checking, ESLint, Prettier
- **Test Integration**: Run unit tests, integration tests before build
- **Security Scanning**: Dependency vulnerability checking
- **Performance Budgets**: Enforce bundle size and performance limits

### Production Hardening
- **Environment Configuration**: Production environment variables and secrets
- **Security Headers**: CSP, HSTS, security-focused build configuration
- **Monitoring Integration**: Error tracking, performance monitoring setup
- **Deployment Readiness**: Docker images, deployment scripts, health checks

## Build Pipeline Integration

### CI/CD Compatibility
```yaml
GitHub Actions:
  - Auto-generates workflow files
  - Optimizes for GitHub's runners
  - Implements caching strategies
  
GitLab CI:
  - Creates .gitlab-ci.yml configuration
  - Docker-based builds with optimization
  - Multi-stage deployment pipelines

Docker:
  - Multi-stage Dockerfiles for optimization
  - Security-focused base images
  - Layer caching for faster builds
```

### Quality Gates (8-Step Validation)
1. **Syntax Validation**: TypeScript, ESLint, framework-specific checks
2. **Type Checking**: Full type validation with error reporting
3. **Linting**: Code quality and style consistency  
4. **Security Scanning**: Dependency vulnerabilities and security issues
5. **Testing**: Unit, integration, and E2E test execution
6. **Performance**: Bundle analysis and performance budget validation
7. **Documentation**: Generated docs and API documentation
8. **Integration**: Deployment readiness and environment validation

## Example Workflows

### Full-Stack Application Build
```bash
/build --production --validate
# Auto-detects: React frontend + Node.js backend
# Orchestrates: Frontend build → API build → Integration tests → Deployment prep
# Validates: Performance budgets, security checks, test coverage
```

### Component Library Build  
```bash
/build component-library --publish
# Optimizes: Tree-shaking, TypeScript declarations, CSS extraction
# Validates: API consistency, documentation generation, breaking changes
# Outputs: NPM-ready package with optimized bundles
```

### Microservices Build
```bash
/build microservices --docker --parallel
# Detects: Multiple service directories
# Coordinates: Parallel builds with dependency ordering
# Outputs: Optimized Docker images with health checks
```

## Build Artifacts & Reporting

### Build Outputs
- **Optimized Assets**: Minified, compressed, cache-friendly files
- **Bundle Reports**: Size analysis, dependency graphs, optimization suggestions
- **Performance Metrics**: Build time, bundle size, load performance
- **Quality Reports**: Test coverage, security scan results, lint reports

### Documentation Generation
- **API Documentation**: Auto-generated from code comments and types
- **Component Documentation**: Storybook, design system documentation
- **Deployment Guides**: Environment setup, configuration, troubleshooting
- **Performance Baselines**: Metrics tracking and regression detection

## Auto-Activation Triggers
- Build-related keywords: "build", "compile", "bundle", "deploy"
- Framework modification or configuration changes
- Performance optimization requests
- Production deployment preparation
- CI/CD pipeline setup or modification
- Package.json or build configuration file changes