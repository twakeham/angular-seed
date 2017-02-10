import os
import sys
import json
import shutil


cwd = os.getcwd()

components = {
    'controller': {
        'path': 'controllers',
        'tmpl': 'controller.tmpl'
    },
    'service': {
        'path': 'services',
        'tmpl': 'service.tmpl'
    },
    'directive': {
        'path': 'directives',
        'tmpl': 'directive.tmpl'
    },
    'factory': {
        'path': 'factories',
        'tmpl': 'factory.tmpl'
    }
}


def _normalise_name(name: str) -> str:
    return ''.join([part.title() for part in name.split('_')])


def _load_template(name: str) -> str:
    with open(os.path.join(cwd, 'templates', name)) as template:
        return template.read()


def _load_module_config(name: str) -> dict:
    mod_path = os.path.join(cwd, 'app', 'modules', name)
    with open(os.path.join(mod_path, 'module.config.json')) as config:
        return json.load(config)


def _save_module_config(name: str, config: dict) -> None:
    mod_path = os.path.join(cwd, 'app', 'modules', name)
    with open(os.path.join(mod_path, 'module.config.json'), 'w') as config_file:
        json.dump(config, config_file)

    _generate_requirements(name)


def create_module(name: str) -> None:
    mod_path = os.path.join(cwd, 'app', 'modules', name)
    if os.path.exists(mod_path):
        print('Module with name {0} already exists!'.format(name))
        sys.exit(1)

    os.mkdir(mod_path)

    module_tmpl = _load_template('module.tmpl')
    with open(os.path.join(mod_path, 'module.js'), 'w') as module:
        module.write(module_tmpl.format(name))

    template_folder = input('Create template folder? (y/n)')
    if template_folder.lower() == 'y':
        os.mkdir(os.path.join(mod_path, 'templates'))

    routes = input('Create routes? (y/n)')
    if routes.lower() == 'y':
        shutil.copyfile(os.path.join(cwd, 'templates', 'routes.tmpl'), os.path.join(mod_path, 'module.routes.js'))

    _save_module_config(name, {'module': name})


def _generate_requirements(name: str) -> None:
    mod_path = os.path.join(cwd, 'app', 'modules', name)
    module_config = _load_module_config(name)
    module_config.pop('module')

    files = ['\'./module.js\'']

    if os.path.exists(os.path.join(mod_path, 'routes.js')):
        files.append('\'./module.routes.js\'')

    for component_type, components in module_config.items():
        for component in components:
            files.append('\'./{0}/{1}\''.format(component_type, component))

    template = _load_template('deps.tmpl')
    with open(os.path.join(mod_path, 'module.deps.js'), 'w') as dependencies:
        dependencies.write(template.format(',\n\t'.join(files)))

    modules_paths = os.listdir('app/modules')

    files = []

    for module_path in modules_paths:
        if os.path.exists(os.path.join(cwd, 'app', 'modules', module_path, 'module.deps.js')):
            files.append('\'./{0}/module.deps.js\''.format(module_path))

    with open(os.path.join('app', 'modules', 'module.deps.js'), 'w') as dependencies:
        dependencies.write(template.format(',\n\t'.join(files)))


def create_component(type: str, name: str) -> None:
    try:
        module, denorm_name = name.split('.')
    except ValueError:
        print('Component name must be in the form of [module].[name]')
        sys.exit(1)

    norm_name = _normalise_name(denorm_name)

    try:
        component_type = components[type]
    except KeyError:
        print('Component type must be one of -\n' + '\n'.join(components.keys()))
        sys.exit(1)

    mod_path = os.path.join(cwd, 'app', 'modules', module)
    if not os.path.exists(mod_path):
        print('Module {0} does not exist'.format(module))
        sys.exit(1)

    component_path = os.path.join(mod_path, component_type['path'])

    module_config = _load_module_config(module)

    if not os.path.exists(component_path):
        os.mkdir(component_path)

    template = _load_template(component_type['tmpl'])
    with open(os.path.join(component_path, '{0}.js'.format(denorm_name)), 'w') as component:
        component.write(template.format(norm_name))
        # figure out templates

    module_components = module_config.get(component_type['path'], [])
    module_components.append(denorm_name)
    module_config[component_type['path']] = module_components

    _save_module_config(module, module_config)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('\n'.join(options.keys()))

    command = sys.argv[1]

    if command == 'module':
        create_module(sys.argv[2])
    else:
        create_component(sys.argv[1], sys.argv[2])

